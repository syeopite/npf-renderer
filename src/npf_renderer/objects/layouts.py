import enum
from typing import NamedTuple, Optional, Sequence

from .attribution import BlogAttribution


class DisplayMode(enum.Enum):
    WEIGHTED = 0
    CAROUSEL = 1
    UNSUPPORTED = 2


class AskLayout(NamedTuple):
    ranges: list[int]
    attribution: Optional[BlogAttribution] = None


class RowLayout(NamedTuple):
    ranges: Sequence[int]
    display_mode: DisplayMode = DisplayMode.WEIGHTED


class Rows(NamedTuple):
    rows: Sequence[RowLayout]
    truncate_after: Optional[int] = None
