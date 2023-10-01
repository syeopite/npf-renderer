from typing import NamedTuple, Optional

from .media_objects import MediaObject


class LinkBlock(NamedTuple):
    url: str

    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    site_name: Optional[str] = None
    display_url: Optional[str] = None
    poster: Optional[MediaObject] = None
