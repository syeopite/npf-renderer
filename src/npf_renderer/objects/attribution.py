from typing import NamedTuple, List, Optional, Union

from .media_objects import MediaObject


class BlogAttribution(NamedTuple):
    # Only UUID is required. The rest are optional but should be present in most cases.
    uuid: str

    url: Optional[str] = None
    name: Optional[str] = None

    avatar: Optional[List[MediaObject]] = None


class PostAttribution(NamedTuple):
    url: str
    post: str
    blog: BlogAttribution


class LinkAttribution(NamedTuple):
    url: str


class AppAttribution(NamedTuple):
    url: str

    app_name: Optional[str] = None
    display_text: Optional[str] = None
    logo: Optional[MediaObject] = None


AttributionTypes = Union[BlogAttribution, PostAttribution, LinkAttribution, AppAttribution]
