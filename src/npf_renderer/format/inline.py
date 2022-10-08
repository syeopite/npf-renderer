import itertools
from typing import List

import dominate.tags, dominate.util

from .. import objects, helpers


class Operations(helpers.CursorIterator):
    def __init__(self, operations):
        super().__init__(operations)
        self.next_start = None

    def next(self):
        status = super().next()
        if status:  # Save a bit of performance.
            if peek := self.peek():
                self.next_start = peek.start

        return status


class InlineFormatter(helpers.CursorIterator):
    """Produces an HTML output from NPF's inline formatting and a string"""
    def __init__(self, string: str, inline_formats: List[objects.inline.INLINE_FMT_TYPES]):
        super().__init__(string)
        self.parent_tag = dominate.tags.div(cls="inline-formatted-content")
        self.string = string

        # Sorting just in case although the tumblr API should already return
        # sorted formatting
        #
        # Each inline format is going to be called an "operation"

        # Returns a list of operations sorted by the start (ascending) and end (descending) of each
        operations = sorted(inline_formats, key=lambda format_op: (format_op.start, -format_op.end))
        self.ops = Operations(operations)

        self.accumulator_string = []

    @property
    def new_format_section(self):
        if self.cursor in (self.ops.current.start, self.ops.next_start):
            return True
        else:
            return False

    def next(self):
        status = super().next()
        if status:
            self.accumulator_string.append(self.current)

        return status

    def perform_operation(self, current_tag, till):
        """Performs a formatting option till the specified ending index"""

        # If this stops then that means either a new formatting section begun (likely while in the midst of ours,
        # aka an overlapping region) or we've reached the end of the string, or the end of the current formatting
        # section (the till argument).
        while not self.new_format_section and not self._at_end and (self.cursor < till):
            self.next()

        # Have we reached the end of our own formatting section?
        if (self.cursor >= till) or self._at_end:
            current_tag.add(dominate.util.text("".join(self.accumulator_string)))
            self.accumulator_string = []

            if till == self.ops.current.end:
                self.ops.next()

            return

        # Should be a new formatting section if we've got this far.
        assert self.new_format_section

        # So we're going to push all of our accumulated letters to the current tag
        # to get ready for the overlapping section
        current_tag.add(dominate.util.text("".join(self.accumulator_string)))
        self.accumulator_string = []

        try:
            self.next()
            self.ops.next()

            # Do we go on for longer than the current operation?
            #
            # If so we'll take care of the current operation first, and any subsequent operations that are still
            # overlapping with us.
            if till > self.ops.current.end:
                while till > self.ops.current.end and not self.ops._at_end:
                    self.route_operations(self.ops.current.end, parent_tag=current_tag)

                # As the above function breaks as soon as we reach the end of the operations list
                # there's a few considerations we need to take
                if self.ops._at_end:
                    # First we need to finish up the current operation if we aren't there yet
                    if self.cursor < self.ops.current.end:
                        self.route_operations(self.ops.current.end, parent_tag=current_tag)

                        # Since there's no more new operations to consume, the only operations left are our parents (if
                        # we're here it definitely means we have parents because otherwise till == self.ops.current.end,
                        # and so we wouldn't even be in this if-else chain in the first place)

                        # Anyway, this means that all that's left to do is to consume letters till we've reached till
                        # and append it to the current tag (aka our parent)
                        while self.cursor < till:
                            self.next()

                        current_tag.add(dominate.util.text("".join(self.accumulator_string)))
                        self.accumulator_string = []
                    else:
                        # We've gone past the end of the last operation which means all that's left is our parent.
                        while self.cursor < till:
                            self.next()

                        current_tag.add(dominate.util.text("".join(self.accumulator_string)))
                        self.accumulator_string = []

            else:
                self.route_operations(till, parent_tag=current_tag)

        except StopIteration:
            pass

    def get_tag_of_operation(self, operation):
        match operation.type:
            case objects.inline.FMTTypes.BOLD:
                return dominate.tags.b(cls="inline-bold")

            case objects.inline.FMTTypes.ITALIC:
                return dominate.tags.i(cls="inline-italics")

            case objects.inline.FMTTypes.STRIKETHROUGH:
                return dominate.tags.s(cls="inline-strikethrough")

            case objects.inline.FMTTypes.SMALL:
                return dominate.tags.small(cls="inline-small")

            case objects.inline.FMTTypes.LINK:
                return dominate.tags.a(href=operation.url, cls="inline-link")

            case objects.inline.FMTTypes.MENTION:
                return dominate.tags.a(href=operation.blog_url, cls="inline-mention")

            case objects.inline.FMTTypes.COLOR:
                return dominate.tags.span(style=f"color: {operation.hex};", cls="inline-color")

    def route_operations(self, till, parent_tag=None):
        """Delegate formatting to specific tags

        Adds result to the given parent_tag or self.parent_tag when unset
        """
        if self._at_end:
            return

        if not parent_tag:
            parent_tag = self.parent_tag

        tag = self.get_tag_of_operation(self.ops.current)

        # Check and handle for same overlaps
        nested_child_tags = []
        while ((peek := self.ops.peek())
               and (peek.start == self.ops.current.start)
               and (peek.end == self.ops.current.end)):
            child_tag = self.get_tag_of_operation(peek)
            self.ops.next()

            nested_child_tags.append(child_tag)

        for child_tag_one, child_tag_two in itertools.pairwise(nested_child_tags):
            child_tag_one.add(child_tag_two)

        # Add first child tag in the list to our main tag, which should have all the others nested within
        # and to save some code we also run perform_operation in here with either the last of the nested_child_tags list
        # as it's the innermost tag, or we just run perform_operation with our normal main tag
        if nested_child_tags:
            tag.add(nested_child_tags[0])

            self.perform_operation(current_tag=nested_child_tags[-1], till=till)
        else:
            self.perform_operation(current_tag=tag, till=till)

        parent_tag.add(tag)

    def format(self):
        # Begin operations iteration
        self.ops.next()

        while not self._at_end:
            if self.new_format_section:
                # Dump the unformatted text we've been collecting into the parent
                self.parent_tag.add(dominate.util.text(''.join(self.accumulator_string)))
                self.accumulator_string = []

                till = self.ops.current.end

                # Consumes the next character, so we don't trigger
                # new_format_section again
                self.next()

                self.route_operations(till)

                # Check for remaining operations in the current cursor position
                while self.ops.current.start <= self.cursor < (till := self.ops.current.end):
                    self.next()
                    self.route_operations(till)

            self.next()

        # Leftovers
        if self.accumulator_string:
            self.parent_tag.add(dominate.util.text("".join(self.accumulator_string)))
            self.accumulator_string = []

        return self.parent_tag

