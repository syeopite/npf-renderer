"""Miscellaneous helper functions and objects"""
import abc


class CursorIterator:
    """Allows iterating through some iterable one-by-one with an extra peek() method """
    def __init__(self, iterable):
        self.__iterable = iterable
        self.__iterable_iter = iter(iterable)

        self.cursor = 0
        self.current = None
        self._iter_length = len(iterable)

    @property
    def _at_end(self):
        """Checks if we have reached the end of the content list"""
        return self._iter_length <= self.cursor

    def next(self):
        """Go to the next element in the iterator and returns True if successful"""
        try:
            self.current = next(self.__iterable_iter)
            self.cursor += 1
        except StopIteration:
            return False

        return True

    def peek(self):
        """Takes a peek at the next element"""
        if self._at_end:
            return False

        return self.__iterable[self.cursor]
