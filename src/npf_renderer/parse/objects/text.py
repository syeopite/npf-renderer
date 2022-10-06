"""Objects representing text content type and all of its option in Tumblr's NPF """

import enum
from typing import NamedTuple,  Union


class InlineFormatType(enum.Enum):
    BOLD = 0
    ITALIC = 1
    STRIKETHROUGH = 2
    SMALL = 3
    LINK = 4
    MENTION = 5
    COLOR = 6


class TextBlockSubtypes(enum.Enum):
    HEADING1 = 0
    HEADING2 = 1
    QUIRKY = 2
    QUOTE = 3
    INDENTED = 4
    CHAT = 5
    ORDERED_LIST_ITEM = 6
    UNORDERED_LIST_ITEM = 7


class InlineBaseTextFormatting(NamedTuple):
    type: InlineFormatType
    start: int
    end: int


class InlineLinkTextFormatting(NamedTuple):
    type: InlineFormatType
    start: int
    end: int
    url: str


class InlineMentionTextFormatting(NamedTuple):
    type: InlineFormatType
    start: int
    end: int

    blog_name: str
    blog_url: str
    blog_uuid: str


class InlineColorTextFormatting(NamedTuple):
    type: InlineFormatType
    start: int
    end: int
    hex: str


INLINE_FMT_TYPES = Union[InlineBaseTextFormatting, InlineLinkTextFormatting,
                         InlineMentionTextFormatting, InlineColorTextFormatting]


class TextBlock(NamedTuple):
    text: str
    subtype: TextBlockSubtypes = None
    indent_level: int = None

    inline_formatting: list[INLINE_FMT_TYPES] = None

