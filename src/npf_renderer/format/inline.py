import itertools
from typing import Sequence, Callable

import dominate.tags
import dominate.util

from .. import objects, helpers


class _OperationsIterator(helpers.CursorIterator):
    """Controlled iterator to iterate through a list of inline formatting operations

    Subclasses the CursorIterator object.
    For more information see parent.

    Extends next() to create two additional attributes:
        next_start: Starting index of next operation
        next_end: Ending index of next operation

    """

    def __init__(self, operations):
        super().__init__(operations)

        if peek := self.peek():
            self.next_start = peek.start
            self.next_end = peek.end
        else:
            self.next_start = None
            self.next_end = None

    def next(self):
        """Extends next() to store next_start and next_end"""
        status = super().next()
        if peek := self.peek():
            self.next_start = peek.start
            self.next_end = peek.end
        else:
            self.next_start = None
            self.next_end = None


class InlineFormatter(helpers.CursorIterator):
    """Formatter for NPF's TextBlock's inline formatting"""

    def __init__(self, string: str, inline_formats: Sequence[objects.inline.INLINE_FMT_TYPES], url_handler: Callable):
        """Initializes InlineFormatter with some string and the formats to apply to it"""
        super().__init__(string)
        self.parent_tag = dominate.tags.span(cls="inline-formatted-content")

        # Sorting just in case although the tumblr API should already return
        # sorted formatting
        #
        # Each inline format is going to be called an "operation"

        # Returns a list of operations sorted by the start (ascending) and end (descending) of each
        self._ops = _OperationsIterator(inline_formats)

        self.url_handler = url_handler

        self._accumulator = []

    @property
    def _reached_next_format_operation(self):
        """Check if we have reached the start of a new format operation"""
        if self.cursor == self._ops.next_start:
            return True
        else:
            return False

    def next(self):
        """Extends next() to append the selected character to the _accumulator attribute"""
        status = super().next()
        if status:
            self._accumulator.append(self.current)

        return status

    def _get_tag_of_operation(self, instruction):
        """Maps an inline formatting instruction to a corresponding HTML tag"""
        match instruction.type_:
            case objects.inline.FMTTypes.BOLD:
                return dominate.tags.b(cls="inline-bold")

            case objects.inline.FMTTypes.ITALIC:
                return dominate.tags.i(cls="inline-italics")

            case objects.inline.FMTTypes.STRIKETHROUGH:
                return dominate.tags.s(cls="inline-strikethrough")

            case objects.inline.FMTTypes.SMALL:
                return dominate.tags.small(cls="inline-small")

            case objects.inline.FMTTypes.COLOR:
                return dominate.tags.span(style=f"color: {instruction.hex};", cls="inline-color")

            case objects.inline.FMTTypes.LINK:
                return dominate.tags.a(href=self.url_handler(instruction.url), cls="inline-link")

            case objects.inline.FMTTypes.MENTION:
                return dominate.tags.a(href=self.url_handler(instruction.blog_url), cls="inline-mention")

    def _calculate_operation_tags(self, operation):
        """Converts a specific operation to corresponding HTML tags

        Returns:
            A tuple (working_tag, root_tag), where the working_tag is the tag in which further nested tags and text
            contents should be appended to, and where root_tag is the tag that should be used when appending the final
            product to a parent.

            For instance:
                 We have a root post tag, stored as "post", and we call this method.
                 working_tag, root_tag = self._calculate_operation_tags(operation)

                 The working tag is the one where we apply text contents and further nested tags to:

                 working_tag.add(dominate.util.text("Some text"))

                 And the root tag is the one that we append to the parent post:
                 post.add(root_tag)

            More often than not the working_tag is exactly the same as the root_tag
        """
        if len(operation.instructions) == 1:
            working_tag = self._get_tag_of_operation(operation.instructions[0])
            root_tag = working_tag
        else:
            nested_child_tags = []

            for ops in operation.instructions:
                nested_child_tags.append(self._get_tag_of_operation(ops))

            for child_tag_one, child_tag_two in itertools.pairwise(nested_child_tags):
                child_tag_one.add(child_tag_two)

            # Operations will be conducted on the innermost tag
            working_tag = nested_child_tags.pop()

            # The outermost nested tag is obviously the root tag
            root_tag = nested_child_tags[0]

        return working_tag, root_tag

    def dump_accumulator_to_tag(self, tag):
        """Dumps and clears everything from the accumulator to the given tag as text."""
        tag.add(dominate.util.text("".join(self._accumulator)))
        self._accumulator = []

    def format(self):
        """Returns a formatted string formatted with the given inline operations"""

        while not self._at_end:
            while self._reached_next_format_operation:
                self._ops.next()

                # Dump the unformatted text we've been collecting into the parent
                self.dump_accumulator_to_tag(self.parent_tag)

                # Handle operation

                working_tag, root_tag = self._calculate_operation_tags(self._ops.current)
                while self.cursor != self._ops.current.end and not self._at_end:
                    self.next()

                self.dump_accumulator_to_tag(working_tag)
                self.parent_tag.add(root_tag)

            self.next()

        self.dump_accumulator_to_tag(self.parent_tag)

        return self.parent_tag
