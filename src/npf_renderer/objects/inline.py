"""Objects storing data for inline formatting used in NPF's Text Content Block"""

import enum
from typing import NamedTuple, Union, Sequence


class FMTTypes(enum.Enum):
    BOLD = 0
    ITALIC = 1
    STRIKETHROUGH = 2
    SMALL = 3
    LINK = 4
    MENTION = 5
    COLOR = 6


class Instruction(NamedTuple):
    """A tuple storing data on various inline formatting options"""

    type_: FMTTypes

    def __lt__(self, other):
        return self.type_.value < other.type_.value


class LinkInstruction(NamedTuple):
    """A tuple storing data on formatting an inline link"""

    type_: FMTTypes
    url: str

    def __lt__(self, other):
        return self.type_.value < other.type_.value


class MentionInstruction(NamedTuple):
    """A tuple storing data on formatting an inline mention of a blog"""

    type_: FMTTypes

    blog_name: str
    blog_url: str
    blog_uuid: str

    def __lt__(self, other):
        return self.type_.value < other.type_.value


class ColorInstruction(NamedTuple):
    """A tuple storing data on formatting colored text"""

    type_: FMTTypes
    hex: str

    def __lt__(self, other):
        return self.type_.value < other.type_.value


class StyleInterval(NamedTuple):
    start: int
    end: int
    instructions: Sequence[Union[Instruction, LinkInstruction, MentionInstruction, ColorInstruction]]


INLINE_FMT_TYPES = Union[Instruction, LinkInstruction, MentionInstruction, ColorInstruction]
