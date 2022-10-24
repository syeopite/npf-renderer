from typing import NamedTuple, List, Optional
from .media_objects import MediaObject
from .attribution import AttributionTypes


class ImageBlock(NamedTuple):
    media: List[MediaObject]

    alt_text: Optional[str] = None
    caption: Optional[str] = None
    colors: Optional[List[str]] = None

    attribution: Optional[AttributionTypes] = None



