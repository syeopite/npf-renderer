import enum
from typing import NamedTuple, List, Optional, Union

from .media_objects import MediaObject


class BlogAttribution(NamedTuple):
    url: str
    name: str
    uuid: str

    avatar: Optional[List[MediaObject]] = None


class PostAttribution(NamedTuple):
    url: str
    post: str
    blog: BlogAttribution


class LinkAttribution(NamedTuple):
    url: str


AttributionTypes = Union[BlogAttribution, PostAttribution, LinkAttribution]
