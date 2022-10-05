"""Objects representing Text content type and all of its option in Tumblr's NPF """

import enum
from typing import NamedTuple


class InlineFormatType(enum.Enum):
    BOLD = 0
    ITALIC = 1
    STRIKETHROUGH = 2
    SMALL = 3
    LINK = 4
    MENTION = 5
    COLOR = 6


class TextBlockSubtypes(enum.Enum):
    heading1 = 0
    heading2 = 1
    quirky = 2
    quote = 3
    indented = 4
    chat = 5
    ordered_list_item = 6
    unordered_list_item = 7


class TextBlock(NamedTuple):
    text: str
    subtype: int = None
    indent_level: int = None


class BaseTextFormatting(NamedTuple):
    start: int
    end: int


class LinkTextFormatting(NamedTuple):
    start: int
    end: int
    url: str


class MentionTextFormatting(NamedTuple):
    start: int
    end: int

    blog_name: str
    blog_url: str
    blog_uuid: str


class ColorTextFormatting(NamedTuple):
    start: int
    end: int
    hex: str

