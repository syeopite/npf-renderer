class Parser:
    """All-in-one parser to process NPF content types

    TODO Make base class with all of these properties for the formatter and parser
    """
    def __init__(self, content):
        self.content_array = content
        self.parsed_result = []

        self.cursor = 0
        self.current = self.content_array[self.cursor]
        self.content_length = len(content)

    @property
    def _at_end(self):
        return self.content_length - 1 == self.cursor

    def __next(self):
        """Moves cursor forward by one and returns the (now) selected element"""
        self.cursor += 1
        self.current = self.content_array[self.cursor]
        return self.current

    def _peek(self):
        """Takes a peek at the next element"""
        if self._at_end:
            return False
        return self.content_array[self.cursor + 1]

    def __prev(self):
        """Moves cursor back by one and returns the (now) selected element"""
        self.cursor -= 1
        self.current = self.content_array[self.cursor]
        return self.current

    def _parse_text(self):
        pass

    def parse(self):
        while not self._at_end:
            pass