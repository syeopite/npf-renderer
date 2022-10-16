import itertools
import collections
import queue
from typing import List

import dominate.tags
import dominate.util

from .. import objects, helpers


class Operations(helpers.CursorIterator):
    def __init__(self, operations):
        super().__init__(operations)
        self.next_start = None
        self.next_end = None

    def next(self):
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

        # TODO document this import variable
        # [[(indice), tag, [nested tag]]
        self.stored_tag_trees = []
        self.priority_operator_queue = queue.Queue()
        self.format_missing = False

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
        """Performs a formatting option till the specified ending index

        Arguments:
            current_tag: The tag in which further nested tags and texts gets applied to
            till: An index at which the perform_operation method should break and stop.

        """

        # If this stops then that means either a new formatting section begun (likely while in the midst of ours,
        # aka an overlapping region) or we've reached the end of the string, or the end of the current formatting
        # section (the till argument).
        while not self.new_format_section and not self._at_end and (self.cursor < till):

            # Handle overlapping regions that starts at the same location as us but end differently.
            #
            # We don't have to check for peek() having the same end as us as that case has already been handled
            # in the route_operations method.
            if self.ops.current.start == self.ops.next_start:
                # While we still last longer than the next operation's ending,
                while till > self.ops.next_end:
                    self.ops.next()
                    # The next operation (or current operation now) is going to be included under us.
                    self.route_operations(self.ops.current.end, current_tag)

                    if (self.ops.current.start != self.ops.next_start) or self.ops._at_end:
                        break

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

            # Remember the current operation if we don't get to perform it before the op iterator advances
            operation_latch = None
            # Only for when the till's operation is supposed to finish before the end of the current one
            if till < self.ops.current.end:
                operation_latch = self.ops.current

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
                # Put on priority and fulfilled as soon as it can
                if operation_latch:
                    self.priority_operator_queue.put(operation_latch)

        except StopIteration:
            pass

    def handle_priority_operation(self):
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

        # First things first we handle the prioity queue if any
        while not self.priority_operator_queue.empty():
            operation = self.priority_operator_queue.get()
            operation_tag = self.get_tag_of_operation(operation)
            # If we're within the new current operation (which we likely are)

            if operation.start <= self.ops.current.end and self.ops.current.start <= operation.end:
                # We'll either run to our ending if we're within the operation
                # or to their ending if they finish first
                if operation.end <= self.ops.current.end:
                    # Either run until the till value or the end of the operation depending on which ends first
                    if till < operation.end:
                        self.route_operations(till, parent_tag=operation_tag)
                        self.priority_operator_queue.put(operation)

                    else:
                        self.route_operations(operation.end, parent_tag=operation_tag)

                    # Sometimes gets terminated early when the child of our child ends before we do. Therefore we'll
                    # finish the remaining if applicable:
                    if self.cursor < operation.end and self.cursor < till:
                        # Of course we might actually have to just run until the till value if it ends before we do
                        if till < operation.end:
                            # Which in that case then it's just a repeat of the logic in self.perform_operation
                            # in which we add the remaining stuff to do to the priority queue
                            self.route_operations(till, parent_tag=operation_tag)
                            self.priority_operator_queue.put(operation)
                        else:
                            self.route_operations(operation.end, parent_tag=operation_tag)
                    elif self.cursor < till == self.ops.current.end:
                        # If we have ended, but we still haven't reached the till value then obviously it goes on for
                        # longer than us. So, in the current context, if we need to finish the operation of the till
                        # value (current op end == till) then we do it. Otherwise, we'll let the outer caller handle it
                        parent_tag.add(operation_tag)

                        return self.route_operations(self.ops.current.end, parent_tag=parent_tag)

                else:
                    self.route_operations(self.ops.current.end, parent_tag=operation_tag)
            else:
                # Not Possible
                raise RuntimeError

            if self._at_end:
                return

            return parent_tag.add(operation_tag)

            # Return if at end

        tag = None  # Jank solution to register tag variable as always available.
        # If reconstruct_nest_tree, tag will always be made right before we run perform_operations

        reconstruct_at = None
        reconstruct_nest_tree = False
        if self.stored_tag_trees and (reconstruct_at := self._match_nest_tree()) is not None:
            reconstruct_nest_tree = True
        else:
            tag = self.get_tag_of_operation(self.ops.current)

        # Check and handle for same overlaps
        nested_child_tags = []
        nested_child_operations = []  # Used to reconstruct this nested china if needed
        first_operation = self.ops.current

        while not self.ops._at_end and ((self.ops.next_start == self.ops.current.start)
                                        and (self.ops.next_end == self.ops.current.end)):
            self.ops.next()
            child_tag = self.get_tag_of_operation(self.ops.current)

            nested_child_tags.append(child_tag)
            nested_child_operations.append(self.ops.current)

        for child_tag_one, child_tag_two in itertools.pairwise(nested_child_tags):
            child_tag_one.add(child_tag_two)

        # Add first child tag in the list to our main tag, which should have all the others nested within
        # and to save some code we also run perform_operation in here with either the last of the nested_child_tags list
        # as it's the innermost tag, or we just run perform_operation with our normal main tag
        if nested_child_tags:
            tag.add(nested_child_tags[0])

            self.stored_tag_trees.append(
                ((first_operation.start, first_operation.end), first_operation, nested_child_operations)
            )

            self.perform_operation(current_tag=nested_child_tags[-1], till=till)
        elif reconstruct_nest_tree:
            nested_child_operations = self.stored_tag_trees.pop(reconstruct_at)
            nested_child_tags = []

            # Repeat of the handling code above
            for ops in nested_child_operations[2]:
                nested_child_tags.append(self.get_tag_of_operation(ops))

            for child_tag_one, child_tag_two in itertools.pairwise(nested_child_tags):
                child_tag_one.add(child_tag_two)

            tag = self.get_tag_of_operation(nested_child_operations[1])
            tag.add(nested_child_tags[0])
            self.perform_operation(current_tag=nested_child_tags[-1], till=till)

            # Add back operations tree in case of further interruptions
            self.stored_tag_trees.append(nested_child_operations)
        else:
            self.perform_operation(current_tag=tag, till=till)

        parent_tag.add(tag)

        return parent_tag

    def _match_nest_tree(self):
        # Attempt to find a match
        matched_index = None
        for index, package in enumerate(self.stored_tag_trees):
            indices = package[0]

            if (self.ops.current.start, self.ops.current.end) == indices:
                matched_index = index
                break

        return matched_index

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
