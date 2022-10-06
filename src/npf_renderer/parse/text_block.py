from .base import BaseNPFParser
from ..objects import text_block, inline


class TextBlockNPFParser(BaseNPFParser):
    """Parses the TextBlock NPF into objects

    The logic works like this. When render_content calls upon the logic in this namespace, it uses the process() method.
    Which attempts to see if the given content is applicable. If it is then it quickly calls parse() with the given
    content and returns the output. If not None is returned then the parsing part of render_content() will quickly
    iterate to the next parser

    """
    @staticmethod
    def process(content):
        if content["type"] == "text":
            return TextBlockNPFParser.parse(content)

    @staticmethod
    def parse(content):
        text = content["text"]
        # Subtype is None if content.get("subtype") doesn't find anything.
        if subtype := content.get("subtype"):
            subtype = getattr(text_block.Subtypes, subtype.upper().replace("-", "_"))

        inline_formats = None
        if inline_formatting := content.get("formatting"):
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

        indent_level = content.get("indent_level")

        return text_block.TextBlock(
            text=text,
            subtype=subtype,
            indent_level=indent_level,

            inline_formatting=inline_formats
        )
