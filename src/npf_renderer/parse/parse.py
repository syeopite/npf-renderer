"""Parses NPF Content blocks into python objects

parser = Parser(content_list)
results = parser.parse()

"""

from ..objects import inline, text_block
from .. import helpers


class Parser(helpers.CursorIterator):
    """All-in-one parser to process NPF content types"""
    def __init__(self, content):
        """Initializes the parser with a list of content blocks (json objects) to parse"""
        super().__init__(content)
        self.parsed_result = []

    def _parse_text(self, nest_level=0):
        """Parses a NPF text content block into a TextBlock

        Takes the selected JSON text content block from `self.current` and parses it into a TextObject.
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
        while peekaboo := self.peek():
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
                self.next()
                nest_array.append(self._parse_text(nest_level=nest_level + 1))
            else:
                # If not however, then they are either our siblings,  in the same level as our parent,
                # or an even "higher" (or lower with regard to indent_level) level; so we'll return and let whoever
                # called us process them (or delegate to higher levels)
                return create_text_block(text, subtype, inline_formats, nest_=nest_array)

        return create_text_block(text, subtype, inline_formats, nest_=nest_array)

    @staticmethod
    def route_inline_format(inline_format, start, end):
        inline_type = getattr(inline.FMTTypes, inline_format["type"].upper())

        match inline_type:
            case (inline.FMTTypes.BOLD | inline.FMTTypes.ITALIC |
                  inline.FMTTypes.STRIKETHROUGH | inline.FMTTypes.SMALL):
                return inline.Standard(
                    start=start,
                    end=end,
                    type=inline_type
                )
            case inline.FMTTypes.LINK:
                return inline.Link(
                    start=start,
                    end=end,
                    type=inline_type,
                    url=inline_format["url"]
                )
            case inline.FMTTypes.MENTION:
                blog = inline_format["blog"]
                return inline.Mention(
                    start=start,
                    end=end,
                    type=inline_type,

                    blog_name=blog["name"],
                    blog_uuid=blog["uuid"],
                    blog_url=blog["url"]
                )
            case inline.FMTTypes.COLOR:
                return inline.Color(
                    start=start,
                    end=end,
                    type=inline_type,

                    hex=inline_format["hex"],
                )

    def _parse_inline_text(self, inline_formatting):
        """Parses the inline formatting of a content block into an array of inline fmt objects"""
        inline_formats = []
        inline_formatting_iter = helpers.CursorIterator(inline_formatting)
        while not inline_formatting_iter._at_end:
            inline_formatting_iter.next()

            inline_format = inline_formatting_iter.current
            start, end = inline_format["start"], inline_format["end"]
            current_parsed_inline_fmt = self.route_inline_format(inline_format, start, end)

            overlapping_formats = []
            while peek := inline_formatting_iter.peek():
                p_start, p_end = peek["start"], peek["end"]

                if start == p_start and end == p_end:
                    overlapping_formats.append(self.route_inline_format(peek, p_start, p_end))
                    inline_formatting_iter.next()

                else:
                    # Tumblr's API should return the list of inline fmts sorted. So if even one doesn't match then
                    # we shouldn't have any overlapping ranges with same start and end
                    break

            if overlapping_formats:
                inline_formats.append(
                    inline.TotalOverlaps(
                        type=[current_parsed_inline_fmt] + overlapping_formats,
                        start=start,
                        end=end
                    )
                )
            else:
                inline_formats.append(current_parsed_inline_fmt)

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
        while self.next():
            self.__parse_block()

        return self.parsed_result
