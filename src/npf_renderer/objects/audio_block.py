from typing import NamedTuple, Sequence, Optional

from .attribution import AttributionTypes
from .media_objects import MediaObject
from .embed_iframe import EmbedIframeObject


class AudioBlock(NamedTuple):
    url: Optional[str] = None
    provider: Optional[str] = None
    media: Optional[Sequence[MediaObject]] = None

    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    poster: Optional[Sequence[MediaObject]] = None

    embed_html: Optional[str] = None
    embed_url: Optional[str] = None

    # Provider specific metadata
    # metadata: Optional[dict] = None

    attribution: Optional[AttributionTypes] = None
    # can_autoplay_on_cellular: Optional[bool] = None
