"""Miscellaneous helper functions and objects"""


class CursorIterator:
    """Allows iterating through some iterable one-by-one with an extra peek() method"""

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


def build_duration_string(tdelta):
    duration_string = ["P"]
    units = []

    days = tdelta.days
    if days:
        duration_string.append(f"{days}D")

    hours, remainder = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours or minutes or seconds:
        duration_string.append("T")

        for num, unit in ((hours, "H"), (minutes, "M"), (seconds, "S")):
            if num:
                duration_string.append(f"{num}{unit}")

    return "".join(duration_string)
