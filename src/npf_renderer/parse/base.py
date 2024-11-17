from typing import Optional
from .. import helpers


class BaseParser(helpers.CursorIterator):
    def __init__(self, content):
        super().__init__(content)
        self.parsed_result = []

    def get(self, key, target=None):
        """Fetches the value that matches the given key from the current block

        Assumes that the current item in iteration is subscriptable
        """
        if not target:
            target = self.current

        if key in target:
            return target[key]

        return None

    def get_or(self, *keys, target=None):
        """Fetches the first value that matches the given keys from the current block

        Assumes that the current item in iteration is subscriptable
        """
        for key in keys:
            value = self.get(key, target)

            if value is not None:
                return value

        return None

    def __parse_next(self):
        pass

    def parse(self):
        """Begins the parsing chain and returns the final list of parsed objects"""
        while self.next():
            self.parsed_result.append(self.__parse_next())

        return self.parsed_result
