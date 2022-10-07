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
        self.parent_tag = dominate.tags.span(cls="inline-formatted-content")
        self.string = string

        # Sorting just in case although the tumblr API should already return
        # sorted formatting
        #
        # Each inline format is going to be called an "operation"

        self.operations = sorted(inline_formats, key=lambda obj: obj.start)
        self.ops = Operations(self.operations)

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
                while till > self.ops.current.end:
                    self.route_operations(self.ops.current.end, parent_tag=current_tag)

                # Finally we can finish the remaining
                self.route_operations(till, parent_tag=current_tag)
            else:
                self.route_operations(till, parent_tag=current_tag)

        except StopIteration:
            pass

    def route_operations(self, till, parent_tag=None):
        """Delegate formatting to corresponding functions till the specified amount.
        Adds result to the given parent_tag or self.parent_tag when unset
        """
        if self._at_end:
            return

        if not parent_tag:
            parent_tag = self.parent_tag

        with parent_tag:
            match self.ops.current.type:
                case objects.inline.FMTTypes.BOLD:
                    self.perform_operation(dominate.tags.b(cls="inline-bold"), till)

                case objects.inline.FMTTypes.ITALIC:
                    self.perform_operation(dominate.tags.i(cls="inline-italics"), till)

                case objects.inline.FMTTypes.STRIKETHROUGH:
                    self.perform_operation(dominate.tags.s(cls="inline-strikethrough"), till)

                case objects.inline.FMTTypes.SMALL:
                    self.perform_operation(dominate.tags.small(cls="inline-small"), till)

                case objects.inline.FMTTypes.LINK:
                    self.perform_operation(dominate.tags.a(href=self.ops.current.url, cls="inline-link"), till)

                case objects.inline.FMTTypes.MENTION:
                    self.perform_operation(dominate.tags.a(href=self.ops.current.blog_url, cls="inline-mention"), till)

                case objects.inline.FMTTypes.COLOR:
                    self.perform_operation(dominate.tags.span(style=f"color: {self.ops.current.hex};",
                                                              cls="inline-color"), till)

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

