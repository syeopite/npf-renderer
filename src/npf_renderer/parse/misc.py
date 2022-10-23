from ..objects import image, attribution


def parse_media_block(media_block):
    """Parses a NPF media object json into a MediaObject NamedTuple"""
    url = media_block["url"]
    mime = media_block.get("type")

    # Defaults to 540x405
    width = media_block.get("width", 540)
    height = media_block.get("height", 405)

    cropped = media_block.get("cropped")

    original_dimensions_missing = media_block.get("original_dimensions_missing")
    has_original_dimensions = media_block.get("has_original_dimensions")

    # Additional checks for the camel case variants
    if not original_dimensions_missing:
        original_dimensions_missing = media_block.get("originalDimensionsMissing")
    if not has_original_dimensions:
        has_original_dimensions = media_block.get("hasOriginalDimensions")

    poster = None
    video = None

    # For some reason they can sometimes be packed into a list with it being the only element.
    if poster_block := media_block.get("poster"):
        poster_block = poster_block[0] if isinstance(poster_block, list) else poster_block
        poster = parse_media_block(poster_block)
    if video_block := media_block.get("video"):
        video_block = video_block[0] if isinstance(video_block, list) else video_block
        video = parse_media_block(video_block)

    return image.MediaObject(
        url=url,
        type=mime,
        width=width,
        height=height,

        original_dimensions_missing=original_dimensions_missing,
        cropped=cropped,
        has_original_dimensions=has_original_dimensions,

        poster=poster,
        video=video
    )
