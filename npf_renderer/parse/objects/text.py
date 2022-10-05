"""Objects representing Text content type and all of its option in Tumblr's NPF """

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
    heading1 = 0
    heading2 = 1
    quirky = 2
    quote = 3
    indented = 4
    chat = 5
    ordered_list_item = 6
    unordered_list_item = 7


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

