import itertools
import queue
from typing import List

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
        self.next_start = None
        self.next_end = None

    def next(self):
        """Extends next() to store next_start and next_end"""
        status = super().next()
        if status:  # Save a bit of performance.
            if peek := self.peek():
                self.next_start = peek.start
                self.next_end = peek.end

        if not status:
            self.next_start = None
            self.next_end = None

        return status


class InlineFormatter(helpers.CursorIterator):
    """Formatter for NPF's TextBlock's inline formatting"""

    def __init__(self, string: str, inline_formats: List[objects.inline.INLINE_FMT_TYPES]):
        """Initializes InlineFormatter with some string and the formats to apply to it """
        super().__init__(string)
        self.parent_tag = dominate.tags.div(cls="inline-formatted-content")

        # Sorting just in case although the tumblr API should already return
        # sorted formatting
        #
        # Each inline format is going to be called an "operation"

        # Returns a list of operations sorted by the start (ascending) and end (descending) of each
        operations = sorted(inline_formats, key=lambda format_op: (format_op.start, -format_op.end))
        self._ops = _OperationsIterator(operations)

        self._accumulator = []

        # Temporarily latches onto operations that needs to be completed
        # in the next context for whatever reasons
        self._priority_operation_queue = queue.Queue()

    @property
    def _reached_new_format_operation(self):
        """Check if we have reached the start of a new format operation"""
        if self.cursor in (self._ops.current.start, self._ops.next_start):
            return True
        else:
            return False

    def next(self):
        """Extends next() to append the selected character to the _accumulator attribute"""
        status = super().next()
        if status:
            self._accumulator.append(self.current)

        return status

    def _perform_operation(self, current_tag, till):
        """Performs a formatting option till the specified ending index

        Arguments:
            current_tag: The tag in which further nested tags and text gets applied/added to
            till: An index at which the perform_operation method should break and stop.

        """

        # If this stops then that means either a new formatting section begun (likely while in the midst of ours,
        # aka an overlapping region) or we've reached the end of the string, or the end of the current formatting
        # section (the till argument).
        while not self._reached_new_format_operation and not self._at_end and (self.cursor < till):

            # Handle overlapping regions that starts at the same location as us but end differently.
            #
            # We don't have to check for peek() also having the same end as those are already condensed into
            # a single operation during the parsing stage.
            if self._ops.current.start == self._ops.next_start:
                # If we (operation or till-wise) still last longer than the next operation
                # then they'll be handled under us.
                while till > self._ops.next_end:
                    self._ops.next()
                    self._route_operations(self._ops.current.end, current_tag)

                    # Obviously we can break once our start differs again or we've reached the end
                    if (self._ops.current.start != self._ops.next_start) or self._ops._at_end:
                        break

            self.next()

        # Have we reached our stopping point? (Doesn't matter whether it's the end of our current op or not)
        # If so we dump into the current tag and let whoever called us handle what comes next or
        # what remains of us if any.
        if (self.cursor >= till) or self._at_end:
            current_tag.add(dominate.util.text("".join(self._accumulator)))
            self._accumulator = []

            # Get next operation if we are completely finished
            if till == self._ops.current.end:
                self._ops.next()

            return

        # It should be a new formatting section if we've got this far.
        assert self._reached_new_format_operation

        # So we're going to push all of our accumulated letters to the current tag
        # to get ready for the overlapping section (The next operation will be starting while we're still in the midst
        # of ours.)
        current_tag.add(dominate.util.text("".join(self._accumulator)))
        self._accumulator = []

        try:
            self.next()

            # If our current operation lasts longer than when this method is supposed to end,
            # and a new formatting operation is starting then we need to make sure that this current operation actually
            # gets remembered and finished once the new formatting section has been taken care of.

            # Without this another formatting section in the midst of the one that's about to start might be
            # reached, and we'll lose access to the current formatting section forever.

            operation_latch = None
            if till < self._ops.current.end:
                operation_latch = self._ops.current

            self._ops.next()

            # Do we go on for longer than the (now) current operation?
            #
            # If so we'll take care of the current operation first, and any subsequent operations that are still
            # overlapping with us.
            if till > self._ops.current.end:
                while till > self._ops.current.end and not self._ops._at_end:
                    self._route_operations(self._ops.current.end, parent_tag=current_tag)

                # As the above function breaks as soon as we reach the end of the operations list
                # there's a few considerations we need to take
                if self._ops._at_end:
                    # First we need to finish up the current operation if we aren't there yet
                    if self.cursor < self._ops.current.end:
                        self._route_operations(self._ops.current.end, parent_tag=current_tag)

                    # Since there's no more new operations to consume, the only operations left to finish is our own.
                    # Therefore, we shall advance up until till (either our stopping point or end of our operation)
                    # and then append the result to current_tag and let whoever called us handle the remaining stuff if
                    # any.
                    while self.cursor < till:
                        self.next()

                    current_tag.add(dominate.util.text("".join(self._accumulator)))
                    self._accumulator = []
                else:
                    # Finish remaining characters until till
                    self._perform_operation(current_tag=current_tag, till=till)

            else:
                self._route_operations(till, parent_tag=current_tag)
                # Read comment above. Dump in priority queue to get fulfilled as soon as we reach route_operations()
                # again, which should be to fulfill the remainder of the current op.
                if operation_latch and till < operation_latch.end:
                    self._priority_operation_queue.put(operation_latch)

        except StopIteration:
            pass

    @staticmethod
    def _get_tag_of_operation(operation):
        """Maps an inline formatting operation to corresponding HTML tags

        This should probably not be used directly. Instead, use _calculate_operation_tags() which calls this method.
        """
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
        if not isinstance(operation.type, list):
            working_tag = self._get_tag_of_operation(operation)
            root_tag = working_tag
        else:
            nested_child_tags = []

            for ops in operation.type:
                nested_child_tags.append(self._get_tag_of_operation(ops))

            for child_tag_one, child_tag_two in itertools.pairwise(nested_child_tags):
                child_tag_one.add(child_tag_two)

            # Operations will be conducted on the innermost tag
            working_tag = nested_child_tags.pop()

            # The outermost nested tag is obviously the root tag
            root_tag = nested_child_tags[0]

        return working_tag, root_tag

    def _perform_priority_operation(self, till, parent_tag):
        """Fetches and performs a priority operation from the priority queue

        The priority operation is an operation that wasn't able to get completed in the last context due to the
        operations iterator advancing past while also having its current context end before reaching the ending point.

        See _perform_operation() for more details on how this method works.
        """

        # Priority queue handling. If something exists within it is likely that the priority operation wasn't able to
        # be completed in the last context due to the operator iterator advancing, and also having reached the till
        # stopping point.
        #
        # For more information see the innards of self.perform_operation
        operation = self._priority_operation_queue.get()
        operation_tag, attachment_tag = self._calculate_operation_tags(operation)

        if operation.start <= self._ops.current.end and self._ops.current.start <= operation.end:
            # If the priority operation ends after the currently selected operation does then we will finish that
            # first. Otherwise, vise versa.
            if operation.end <= self._ops.current.end:
                # Either run until the till value or the end of the priority operation depending on which ends first
                if till < operation.end:
                    self._route_operations(till, parent_tag=operation_tag)

                    # Latch current operation to be handled the next time we reach self.route_operation
                    # since our current context needs to end as we've reached till, and we still haven't reached
                    # operation.end
                    self._priority_operation_queue.put(operation)
                else:
                    self._route_operations(operation.end, parent_tag=operation_tag)

                # If somehow we've neither hit the end of the priority operation, or even till then we'll
                # need to finish off the remainders
                if self.cursor < operation.end and self.cursor < till:
                    # Of course, we might actually have to just run until the till value if it ends before we do
                    if till < operation.end:
                        self._route_operations(till, parent_tag=operation_tag)
                        # So we also latch onto the priority operation as our current context is ending forcing us
                        # to finish in the next context instead
                        self._priority_operation_queue.put(operation)
                    else:
                        self._route_operations(operation.end, parent_tag=operation_tag)

                elif self.cursor < till == self._ops.current.end:
                    # If we have ended, but we still haven't reached the till value then obviously it goes on for
                    # longer than the priority operation. As such we need to finish that.

                    # We just need to make sure that we are working in the same context as what the till
                    # operation should be. It can be checked by a comparison of (till == self.ops.current.end)

                    parent_tag.add(attachment_tag)

                    return self._route_operations(self._ops.current.end, parent_tag=parent_tag)
            else:
                # Since we (the priority operation) last longer than the currently selected operation, we're going
                # to finish it (and any other operations that remains inside us) until we've reached our breaking
                # point of till
                while till < operation.end and not self._ops._at_end:
                    self._route_operations(self._ops.current.end, parent_tag=operation_tag)

                if self._ops._at_end:
                    if self.cursor < till:
                        self._route_operations(till, parent_tag=operation_tag)

                    # We've already processed until the till, and now we're also at the end of the operations list.
                    # There shouldn't be anything more to do. We will directly process until the end of the current
                    # priority operation
                    while self.cursor < operation.end:
                        self.next()

                    operation_tag.add(dominate.util.text("".join(self._accumulator)))
                    self._accumulator = []

                else:
                    # Finish remaining if applicable
                    if self.cursor < till:
                        self._route_operations(till, parent_tag=operation_tag)

                    # If we've reached the end of our current context and still haven't completed the priority
                    # operation then we'll just do it next time we reach self.route_operations
                    if till < operation.end:
                        self._priority_operation_queue.put(operation)
        else:
            # Not Possible
            raise RuntimeError

        if self._at_end:
            return

        return parent_tag.add(attachment_tag)

    def _route_operations(self, till, parent_tag=None):
        """Delegate formatting to specific tags

        Adds result to the given parent_tag or self.parent_tag when unset
        """
        if self._at_end:
            return

        if not parent_tag:
            parent_tag = self.parent_tag

        if not self._priority_operation_queue.empty():
            return self._perform_priority_operation(till, parent_tag)

        working_tag, attachment_tag = self._calculate_operation_tags(self._ops.current)
        self._perform_operation(current_tag=working_tag, till=till)

        parent_tag.add(attachment_tag)

    def format(self):
        """Returns a formatted string formatted with the given inline operations"""

        # Begin operations iteration
        self._ops.next()

        while not self._at_end:
            if self._reached_new_format_operation:
                # Dump the unformatted text we've been collecting into the parent
                self.parent_tag.add(dominate.util.text(''.join(self._accumulator)))
                self._accumulator = []

                till = self._ops.current.end

                # Consumes the next character, so we don't trigger
                # new_format_section again
                self.next()
                self._route_operations(till)

                # Check for remaining operations in the current cursor position
                while self._ops.current.start <= self.cursor < (till := self._ops.current.end):
                    self.next()
                    self._route_operations(till)

            # Handle remaining priority queue
            if not self._priority_operation_queue.empty():
                # Inefficient way to get a till value.
                operation = self._priority_operation_queue.get()
                till = operation.end
                self._priority_operation_queue.put(operation)

                # Will reaccess the priority operator queue inside
                self._route_operations(till)

            self.next()

        # Leftovers
        if self._accumulator:
            self.parent_tag.add(dominate.util.text("".join(self._accumulator)))
            self._accumulator = []

        return self.parent_tag
