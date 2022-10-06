"""Parses NPF Content blocks into python objects

parser = Parser(content_list)
results = parser.parse()

"""

from ..objects import inline, text_block


class Parser:
    """All-in-one parser to process NPF content types

    TODO Make base class with all of these properties for the formatter and parser
    """
    def __init__(self, content):
        """Initializes the parser with a list of content blocks (json objects) to parse"""
        self.content_list = content
        self.parsed_result = []

        self.cursor = 0
        self.current = self.content_list[self.cursor]
        self.content_length = len(content)  # Prevents calculating len(self.content_list) over and over again

    @property
    def _at_end(self):
        """Checks if we have reached the end of the content list"""
        return self.content_length - 1 == self.cursor

    def __next(self):
        """Moves cursor forward by one and returns the (now) selected element"""
        self.cursor += 1
        self.current = self.content_list[self.cursor]
        return self.current

    def _peek(self):
        """Takes a peek at the next element"""
        if self._at_end:
            return False
        return self.content_list[self.cursor + 1]

    def __prev(self):
        """Moves cursor back by one and returns the (now) selected element"""
        self.cursor -= 1
        self.current = self.content_list[self.cursor]
        return self.current

    def _parse_text(self, nest_level=0):
        """Parses a NPF text content block into a TextBlock

        Takes the selected JSON text content block from self.current and parses it into a TextObject.
        Accepts a nest_level argument to handle any nesting.

        Args:
            nest_level: An argument representing how nested the current text block is in relations with other text
        blocks. In the original NPF this is represented as the indent_level. You should probably not be calling this
        method with that argument set as anything other than zero.

        Returns:
            'TextBlock' See documentation for that object for more information
        """
        def create_text_block(text_, subtype_, inline_formatting_, nest_=None):
            """Create a TextBlock object based on the data we have parsed"""
            if not nest_:
                nest_ = None

            return text_block.TextBlock(
                text=text_,
                subtype=subtype_,
                nest=nest_,
                inline_formatting=inline_formatting_,
            )

        text = self.current["text"]
        if subtype := self.current.get("subtype"):
            subtype = getattr(text_block.Subtypes, subtype.upper().replace("-", "_"))

        inline_formats = None
        if inline_formatting := self.current.get("formatting"):
            inline_formats = self._parse_inline_text(inline_formatting)

        # Begins the check to see if we have any children in the next element(s)
        nest_array = []
        while peekaboo := self._peek():
            # Our children can only be TextBlock and ones with a set indent_level attr (which implies that they are
            # related to us)
            #
            # When an indent_level attr is set, we should also probably either be one of the list subtypes or a indented
            # block quote subtype. This check shouldn't be needed, however.
            if peekaboo["type"] != "text" or not (indent_level := peekaboo.get("indent_level")):
                return create_text_block(text, subtype, inline_formats, nest_array)

            # If the next element's indent level is higher than ours (stored as nest_level), they are our children.
            # Thus, we'll store them under us.
            if indent_level > nest_level:
                self.__next()
                nest_array.append(self._parse_text(nest_level=nest_level + 1))
            else:
                # If not however, then they are either our siblings,  in the same level as our parent,
                # or an even "higher" (or lower with regard to indent_level) level; so we'll return and let whoever
                # called us process them (or delegate to higher levels)
                return create_text_block(text, subtype, inline_formats, nest_=nest_array)

        return create_text_block(text, subtype, inline_formats, nest_=nest_array)

    @staticmethod
    def _parse_inline_text(inline_formatting):
        """Parses the inline formatting of a content block into an array of inline fmt objects"""
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
        """Parses a content block and appends the result to self.parsed_result

        Works by routing specific content types to corresponding parse methods
        """
        match self.current["type"]:
            case "text":
                block = self._parse_text()
                self.parsed_result.append(block)

    def parse(self):
        """Begins the parsing chain and returns the final list of parsed objects"""
        while not self._at_end:
            self.__parse_block()
            self.__next()

        # at_end declares that everything ended as soon as the cursor reached the last value
        # which means that the last element gets skipped. So we'll do it here: TODO fix this logic
        self.__parse_block()

        return self.parsed_result
