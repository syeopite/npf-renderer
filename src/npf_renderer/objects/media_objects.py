from typing import NamedTuple


class MediaObject(NamedTuple):
    """NamedTuple representing Tumblr's NPF Media Object"""
    url: str  # URL to the media in question
    type: str  # MIME type
    width: int  # Default: 540
    height: int  # Default: 405

    original_dimensions_missing: bool = None  # If original dimensions are missing
    cropped: bool = None  # If media object is cropped
    has_original_dimensions: bool = None  # If object has the same dimensions as the original media
