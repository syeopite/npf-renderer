"""Object representing NPF's Text Content Block

For inline formatting stuff see the adjacent inline.py
"""

import enum
from typing import NamedTuple

from .inline import INLINE_FMT_TYPES


class Subtypes(enum.Enum):
    """Enum representing NPF's Text Block's subtype values"""
    HEADING1 = 0
    HEADING2 = 1
    QUIRKY = 2
    QUOTE = 3
    INDENTED = 4
    CHAT = 5
    ORDERED_LIST_ITEM = 6
    UNORDERED_LIST_ITEM = 7


class TextBlock(NamedTuple):
    """Object representing Tumblr's NPF's Text Block"""
    text: str
    subtype: Subtypes = None
    nest: 'list[TextBlock]' = None

    inline_formatting: list[INLINE_FMT_TYPES] = None

