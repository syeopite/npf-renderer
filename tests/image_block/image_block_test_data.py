import dominate.tags

from npf_renderer import objects


def format_constructor(*children):
    return dominate.tags.div(
        dominate.tags.figure(dominate.tags.div(*children, cls="image-container"), cls="image-block"), cls="post"
    )


basic_image_block = (
    [
        {
            "type": "image",
            "media": [
                {
                    "type": "image/jpeg",
                    "url": "http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90"
                           "/tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg",
                    "width": 1280,
                    "height": 1073
                },
                {
                    "type": "image/jpeg",
                    "url": "http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90"
                           "/tumblr_nshp8oVOnV1rg0s9xo1_540.jpg",
                    "width": 540,
                    "height": 400
                },
                {
                    "type": "image/jpeg",
                    "url": "http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90"
                           "/tumblr_nshp8oVOnV1rg0s9xo1_250.jpg",
                    "width": 250,
                    "height": 150
                }
            ],
            "alt_text": "Sonic the Hedgehog and friends",
            "caption": "I'm living my best life on earth."
        }
    ],
    [
        objects.image.ImageBlock(
            media=[
                objects.media_objects.MediaObject(
                    url='http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/'
                        'tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg',
                    type='image/jpeg',
                    width=1280,
                    height=1073,
                ),
                objects.media_objects.MediaObject(
                    url='http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/'
                        'tumblr_nshp8oVOnV1rg0s9xo1_540.jpg',
                    type='image/jpeg',
                    width=540,
                    height=400,
                ),
                objects.media_objects.MediaObject(
                    url='http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/'
                        'tumblr_nshp8oVOnV1rg0s9xo1_250.jpg',
                    type='image/jpeg',
                    width=250,
                    height=150,
                )
            ],
            alt_text='Sonic the Hedgehog and friends',
            caption="I'm living my best life on earth.",
        )
    ],

    dominate.tags.div(
        dominate.tags.figure(dominate.tags.div(
            dominate.tags.img(
                srcset="http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg "
                       "1280w, http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_540"
                       ".jpg 540w, http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90"
                       "/tumblr_nshp8oVOnV1rg0s9xo1_250.jpg 250w",
                alt="Sonic the Hedgehog and friends",
                cls="image"
            ), cls="image-container"),

            dominate.tags.figcaption(
                "I'm living my best life on earth.",
                cls="image-caption"
            ),

            cls="image-block"
        ),

        cls="post"
    )
)

basic_gif_image_block = (
    [
        {
            "type": "image",
            "media": [
                {
                    "type": "image/gif",
                    "url": "http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90"
                           "/tumblr_nshp8oVOnV1rg0s9xo1_250.gif",
                    "width": 250,
                    "height": 200
                }
            ],
        }
    ],
    [
        objects.image.ImageBlock(
            media=[
                objects.media_objects.MediaObject(
                    url='http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/'
                        'tumblr_nshp8oVOnV1rg0s9xo1_250.gif',
                    type='image/gif',
                    width=250,
                    height=200,
                )
            ],
        )
    ],

    format_constructor(
        dominate.tags.img(
            srcset="http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/"
                   "tumblr_nshp8oVOnV1rg0s9xo1_250.gif 250w",
            cls="image",
            alt="image",
        ),
    )

)

image_block_with_color_attr = (
    [
        {
            "type": "image",
            "media": [
                {
                    "type": "image/jpeg",
                    "url": "http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg",
                    "width": 1280,
                    "height": 1073
                }
            ],
            "colors": {
                "c0": "a24615",
                "c1": "ff7c00"
            }
        }
    ],
    [
        objects.image.ImageBlock(
            media=[
                objects.media_objects.MediaObject(
                    url='http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/'
                        'tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg',
                    type='image/jpeg',
                    width=1280,
                    height=1073,
                )
            ],
            colors=['a24615', 'ff7c00']
        )
    ],

    format_constructor(
        dominate.tags.img(
            srcset="http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/"
                   "tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg 1280w",
            cls="image",
            alt="image",
        ),
    )
)

gif_image_block_with_poster = (
    [
        {
            "type": "image",
            "media": [
                {
                    "type": "image/gif",
                    "url": "https://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_500.gif",
                    "width": 500,
                    "height": 400,
                    "poster": {
                        "type": "image/jpeg",
                        "url": "https://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_500.jpg",
                        "width": 500,
                        "height": 400
                    }
                }
            ]
        }
    ],

    [
        objects.image.ImageBlock(
            media=[
                objects.media_objects.MediaObject(
                    url='https://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/'
                        'tumblr_nshp8oVOnV1rg0s9xo1_500.gif',
                    type='image/gif',
                    width=500,
                    height=400,
                    poster=objects.media_objects.MediaObject(
                        url='https://69.media.tumblr.com/'
                            'b06fe71cc4ab47e93749df060ff54a90/'
                            'tumblr_nshp8oVOnV1rg0s9xo1_500.jpg',
                        type='image/jpeg',
                        width=500,
                        height=400,
                    ),
                )
            ],
        )
    ],

    format_constructor(
        dominate.tags.img(
            srcset="https://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/"
                   "tumblr_nshp8oVOnV1rg0s9xo1_500.gif 500w",
            cls="image",
            alt="image",
        ),
    )
)

gif_image_block_with_post_attribution = (
    [
        {
            "type": "image",
            "media": [
                {"width": 357, "height": 174, "url": "https://64.media.tumblr.com/s400x600/blahblahblah.gifv"},
                {"width": 250, "height": 122, "url": "https://64.media.tumblr.com/s250x400/blahblahblah.gifv"},
            ],
            "attribution": {
                "type": "post",
                "url": "https://example-blog.tumblr.com/post/1234567890/example-gif-post",
                "post": {"id": "1234567890"},
                "blog": {
                    "name": "example-blog",
                    "url": "https://example-blog.tumblr.com",
                    "uuid": "t:SX31hFaWHA_312_df"
                },
            },
            "colors": {"c0": "000000", "c1": "2a1300", "c2": "ffe41a", "c3": "6b4108", "c4": "d74301"}
        }
    ],

    [objects.image.ImageBlock(
        media=[
            objects.media_objects.MediaObject(url="https://64.media.tumblr.com/s400x600/blahblahblah.gifv", width=357,
                                              height=174),
            objects.media_objects.MediaObject(url="https://64.media.tumblr.com/s250x400/blahblahblah.gifv", width=250,
                                              height=122)
        ],

        colors=["000000", "2a1300", "ffe41a", "6b4108", "d74301"],
        attribution=objects.attribution.PostAttribution(
            url="https://example-blog.tumblr.com/post/1234567890/example-gif-post",
            post="1234567890",
            blog=objects.attribution.BlogAttribution(
                name="example-blog",
                url="https://example-blog.tumblr.com",
                uuid="t:SX31hFaWHA_312_df"
            )
        )
    )]
)


# Taken from the JSON data for https://davidragifs.com/post/671497799018381312/big-cat-little-cat
# Slightly edited
gif_image_block_with_link_attribution = (
    [
        {
            "type": "image",
            "media": [
                {
                    "mediaKey": "0655920c23ca997bf6145c32bda00cc5:14ab5a4c91df05c8-c8",
                    "type": "image/webp",
                    "width": 500,
                    "height": 700,
                    "url": "https://64.media.tumblr.com/0655920c23ca997bf6145c32bda00cc5/14ab5a4c91df05c8-c8/s500x750"
                           "/23f1c831d79fb51b56bbd52ae7d8c03336fd6f25.gifv",
                    "colors": {
                        "c0": "15120b",
                        "c1": "2d3e47"
                    },
                    "hasOriginalDimensions": True
                },
            ],
            "attribution": {
                "type": "link",
                "url": "https://davidragifs.com",
                "urlRedirect": "https://href.li/?https://davidragifs.com"
            },
            "colors": {
                "c0": "15120b",
                "c1": "2d3e47"
            }
        },
    ],

    [objects.image.ImageBlock(
        media=[objects.media_objects.MediaObject(
            url="https://64.media.tumblr.com/0655920c23ca997bf6145c32bda00cc5/14ab5a4c91df05c8-c8/s500x750"
                "/23f1c831d79fb51b56bbd52ae7d8c03336fd6f25.gifv",
            width=500,
            height=700,
            type="image/webp",

            has_original_dimensions=True
        )],
        colors=["15120b", "2d3e47"],
        attribution=objects.attribution.LinkAttribution(url="https://davidragifs.com")
    )]
)

