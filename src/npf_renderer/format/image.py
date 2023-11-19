import dominate.tags

from . import attribution
from .. import objects


def create_srcset(media_blocks, url_handler):
    """Renders an array of media blocks into a usable srcset data. Contains the content's srcset and also poster's

    Returns:
        A tuple of the main content's srcset and also the poster's if available
    """
    main_srcset = []

    for image in media_blocks:
        main_srcset.append(f"{url_handler(image.url)} {image.width}w")

    return main_srcset


def format_image(image_block, row_length=1, url_handler=None, skip_cropped_images=False):
    """Renders a ImageBlock into HTML"""
    container_attributes = {
        "cls": "image-container"
    }

    # Disabled. We cannot generate a gradient background that takes up the same amount of space as the browser-selected
    # responsive image as we do not know which image the browser is going to pick. Therefore, we shall skip this part.

    # if image_block.colors:
    #     colors = [f"#{color}" for color in image_block.colors]
    #     container_attributes["style"] = f"background: linear-gradient(to left bottom, {', '.join(colors)});"

    container = dominate.tags.div(**container_attributes)

    if not url_handler:
        def url_handler(url):
            return url

    processed_media_blocks = []

    # Fetch the media object with the original dimensions to be used as a src= attribute
    original_media = None
    for media in image_block.media:
        if skip_cropped_images and media.cropped:
            continue

        processed_media_blocks.append(media)

        if media.has_original_dimensions:
            original_media = media

    # If for whatever reason we cannot the media object with the original dimensions
    # we'd just use the one with the highest res (default)

    original_media = original_media or processed_media_blocks[0]

    container.add(
        dominate.tags.img(
            src=url_handler(original_media.url),
            srcset=", ".join(create_srcset(processed_media_blocks, url_handler)),
            cls="image", loading="lazy",
            alt=image_block.alt_text or "image",
            sizes=f"(max-width: 540px) {int(100 / row_length)}vh, {int(540 / row_length)}px"
        )
    )

    # Add attribution HTML
    if attr := image_block.attribution:
        if isinstance(attr, objects.attribution.LinkAttribution):
            container.add(attribution.format_link_attribution(attr, url_handler))
        elif isinstance(attr, objects.attribution.PostAttribution):
            container.add(attribution.format_post_attribution(attr, url_handler))
        elif isinstance(attr, objects.attribution.AppAttribution):
            container.add(attribution.format_app_attribution(attr, url_handler))
        else:
            # TODO Add "Unsupported Attribution HTML"
            raise RuntimeError

    # Similar to the reason above, we won't be able to hide the poster image once the main content loads.
    # if poster_srcset:
    #     container.add(dominate.tags.img(
    #         srcset=", ".join(poster_srcset),
    #         cls="poster",
    #         style="position: absolute; left:0; top:0;"
    #
    #     ))

    return container
