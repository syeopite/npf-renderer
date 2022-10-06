"""Objects storing data for inline formatting used in NPF's Text Content Block"""

import enum
from typing import NamedTuple, Union


class FMTTypes(enum.Enum):
    BOLD = 0
    ITALIC = 1
    STRIKETHROUGH = 2
    SMALL = 3
    LINK = 4
    MENTION = 5
    COLOR = 6


class Standard(NamedTuple):
    """A tuple storing data on various inline formatting options"""
    type: FMTTypes
    start: int
    end: int


class Link(NamedTuple):
    """A tuple storing data on formatting an inline link"""
    type: FMTTypes
    start: int
    end: int
    url: str


class Mention(NamedTuple):
    """A tuple storing data on formatting an inline mention of a blog"""
    type: FMTTypes
    start: int
    end: int

    blog_name: str
    blog_url: str
    blog_uuid: str


class Color(NamedTuple):
    """A tuple storing data on formatting colored text"""
    type: FMTTypes
    start: int
    end: int
    hex: str


INLINE_FMT_TYPES = Union[Standard, Link, Mention, Color]
