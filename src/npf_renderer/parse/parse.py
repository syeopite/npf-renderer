from ..objects import inline, text_block


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
        text = self.current["text"]
        if subtype := self.current.get("subtype"):
            subtype = getattr(text_block.Subtypes, subtype.upper().replace("-", "_"))

        inline_formats = None
        if inline_formatting := self.current.get("formatting"):
            inline_formats = self._parse_inline_text(inline_formatting)

        indent_level = self.current.get("indent_level")

        return text_block.TextBlock(
            text=text,
            subtype=subtype,
            indent_level=indent_level,
            inline_formatting=inline_formats
        )

    @staticmethod
    def _parse_inline_text(inline_formatting):
        inline_formats = []
        for inline_format in inline_formatting:
            start, end = inline_format["start"], inline_format["end"]
            inline_type = getattr(inline.FMTTypes, inline_format["type"].upper())

            match inline_type:
                case (inline.FMTTypes.BOLD | inline.FMTTypes.ITALIC |
                      inline.FMTTypes.STRIKETHROUGH | inline.FMTTypes.SMALL):
                    inline_formats.append(inline.Standard(
                        start=start,
                        end=end,
                        type=inline_type
                    ))
                case inline.FMTTypes.LINK:
                    inline_formats.append(inline.Link(
                        start=start,
                        end=end,
                        type=inline_type,
                        url=inline_format["url"]
                    ))
                case inline.FMTTypes.MENTION:
                    blog = inline_format["blog"]
                    inline_formats.append(inline.Mention(
                        start=start,
                        end=end,
                        type=inline_type,

                        blog_name=blog["name"],
                        blog_uuid=blog["uuid"],
                        blog_url=blog["url"]
                    ))
                case inline.FMTTypes.COLOR:
                    inline_formats.append(inline.Color(
                        start=start,
                        end=end,
                        type=inline_type,

                        hex=inline_format["hex"],
                    ))

        return inline_formats

    def __parse_block(self):
        match self.current["type"]:
            case "text":
                block = self._parse_text()
                self.parsed_result.append(block)

    def parse(self):
        while not self._at_end:
            self.__parse_block()
            self.__next()

        # at_end declares that everything ended as soon as the cursor reached the last value
        # which means that the last element gets skipped. So we'll do it here: TODO fix this logic
        self.__parse_block()

        return self.parsed_result
