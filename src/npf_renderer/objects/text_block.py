"""Object representing NPF's Text Content Block

For inline formatting stuff see the adjacent inline.py
"""

import enum
from typing import NamedTuple, Sequence, Union

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


ListsSubtype = (Subtypes.ORDERED_LIST_ITEM, Subtypes.UNORDERED_LIST_ITEM)


class TextBlock(NamedTuple):
    """Object representing Tumblr's NPF's Text Block"""

    text: str
    subtype: Subtypes = None
    nest: "Sequence[Union[TextBlock, ListGrouping]]" = None

    inline_formatting: Sequence[INLINE_FMT_TYPES] = None


class ListGrouping(NamedTuple):
    """Groups list item TextBlocks of the same type together to create either an ul or ol element"""

    # We reuse ORDERED_LIST_ITEM and UNORDERED_LIST_ITEM to denote which type we should use
    type: Subtypes
    group: Sequence[TextBlock]
