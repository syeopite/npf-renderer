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

def format_image(image_block, row_length=1, url_handler=lambda url: url, 
                 override_padding=None, original_media=None):
    """Renders a ImageBlock into HTML"""

    container_attributes = {
        "cls": "image-container"
    }

    image_attributes = {}

    # Disabled. We cannot generate a gradient background that takes up the same amount of space as the browser-selected
    # responsive image as the image doesn't really have a size until its loaded and as such neither will the background.
    #
    # In addition some images do not have a colors attribute even though a consistent gradient image is still being 
    # generated on Tumblr's UI, and it is also consistent across reloads. Some investigation is needed on this part

    # if image_block.colors:
    #     colors = [f"#{color}" for color in image_block.colors]
    #     container_attributes["style"] = f"background: linear-gradient(to left bottom, {', '.join(colors)});"

    processed_media_blocks = []

    # Whether or not to preserve image space based on the aspect ratio
    pad = True

    # Skip cropped images and attempt to fetch the media object with the
    # original dimensions to be used in the src= attribute
    if not original_media:
        for media in image_block.media:
            if media.cropped:
                continue

            processed_media_blocks.append(media)

            if media.has_original_dimensions:
                original_media = media

        # If for whatever reason we cannot fetch the media object with the original dimensions
        # we'd just use the one with the highest res
        try:
            original_media = original_media or processed_media_blocks[0]
        except IndexError:
            # Bugged image where the original media is also cropped... for some reason
            original_media = image_block.media[0]

            # I'm not entirely show how common these images are, but they do exist and with the way
            # npf-renderer renders them, they look weird being stretched to the full width of the post when
            # their actual size is a 1px by 1px black pixel for example
            #
            # TODO find more examples of these bugged images and find a proper solution
            # Perhaps this could be a RenderDisclaimerError ? The post itself is fine. It is just weird.
            image_attributes["style"] = f"width: {original_media.width}px; height: {original_media.height}px;"
            pad = False

    if pad:
        if override_padding:
            container_attributes["style"] = f"padding-bottom: {override_padding}%;"
        else:
            height, width = original_media.height, original_media.width
            container_attributes["style"] = f"padding-bottom: {round((height / width) * 100, 4)}%;"

    container = dominate.tags.div(**container_attributes)

    container.add(
        dominate.tags.img(
            src=url_handler(original_media.url),
            srcset=", ".join(create_srcset(processed_media_blocks, url_handler)),
            cls="image", loading="lazy",
            alt=image_block.alt_text or "image",
            sizes=f"(max-width: 540px) {int(100 / row_length)}vh, {int(540 / row_length)}px",
            **image_attributes
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
            raise ValueError(f"Unable to format unsupported attribution: \"{attr}\" ")

    # Similar to the reason above, we won't be able to hide the poster image once the main content loads.
    # if poster_srcset:
    #     container.add(dominate.tags.img(
    #         srcset=", ".join(poster_srcset),
    #         cls="poster",
    #         style="position: absolute; left:0; top:0;"
    #
    #     ))

    return container
