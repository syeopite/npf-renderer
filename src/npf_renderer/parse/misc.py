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
        video=video,
    )


def parse_attribution(attribution_block):
    """Parses a NPF attribution object into corresponding Attribution NamedTuple objects"""
    type_ = attribution_block["type"]

    match type_:
        case "post":
            blog = attribution_block["blog"]
            return attribution.PostAttribution(
                url=attribution_block["url"],
                post=attribution_block["post"]["id"],
                blog=attribution.BlogAttribution(uuid=blog["uuid"], url=blog.get("url"), name=blog.get("name")),
            )

        case "link":
            return attribution.LinkAttribution(
                url=attribution_block["url"],
            )
        case "blog":
            blog = attribution_block["blog"]
            if avatars := blog.get("avatar"):
                avatars = [parse_media_block(avatar) for avatar in avatars]
            else:
                avatars = None

            return attribution.BlogAttribution(
                uuid=blog["uuid"], url=attribution_block.get("url"), name=blog.get("name"), avatar=avatars
            )
        case "app":
            if logo := attribution_block.get("logo"):
                logo = parse_media_block(logo)

            url = attribution_block["url"]
            name = attribution_block.get("app_name")
            display_text = attribution_block.get("display_text")

            # Camel case variant checks
            if not name:
                name = attribution_block.get("appName")
            if not display_text:
                display_text = attribution_block.get("displayText")

            return attribution.AppAttribution(url=url, app_name=name, display_text=display_text, logo=logo)
        case _:
            return attribution.UnsupportedAttribution(type_=type_)
