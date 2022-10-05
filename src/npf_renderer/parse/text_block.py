from .base import BaseNPFParser
from .objects import text as models


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
            subtype = getattr(models.TextBlockSubtypes, subtype.replace("-", "_"))

        inline_formats = None
        if inline_formatting := content.get("formatting"):
            inline_formats = []
            for inline_format in inline_formatting:
                start, end = inline_format["start"], inline_format["end"]
                inline_type = getattr(models.InlineFormatType, inline_format["type"].upper())

                match inline_type:
                    case (models.InlineFormatType.BOLD | models.InlineFormatType.ITALIC |
                          models.InlineFormatType.STRIKETHROUGH | models.InlineFormatType.SMALL):
                        inline_formats.append(models.InlineBaseTextFormatting(
                            start=start,
                            end=end,
                            type=inline_type
                        ))
                    case models.InlineFormatType.LINK:
                        inline_formats.append(models.InlineLinkTextFormatting(
                            start=start,
                            end=end,
                            type=inline_type,
                            url=inline_format["url"]
                        ))
                    case models.InlineFormatType.MENTION:
                        blog = inline_format["blog"]
                        inline_formats.append(models.InlineMentionTextFormatting(
                            start=start,
                            end=end,
                            type=inline_type,

                            blog_name=blog["name"],
                            blog_uuid=blog["uuid"],
                            blog_url=blog["url"]
                        ))
                    case models.InlineFormatType.COLOR:
                        inline_formats.append(models.InlineColorTextFormatting(
                            start=start,
                            end=end,
                            type=inline_type,

                            hex=inline_format["hex"],
                        ))

        indent_level = content.get("indent_level")

        return models.TextBlock(
            text=text,
            subtype=subtype,
            indent_level=indent_level,

            inline_formatting=inline_formats
        )
