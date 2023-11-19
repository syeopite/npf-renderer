import dominate.tags

from npf_renderer import objects


def format_constructor(*children):
    return dominate.tags.div(
        dominate.tags.figure(dominate.tags.div(*children, cls="image-container"), cls="image-block"), cls="post-body"
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
                src="http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg",
                srcset="http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg "
                       "1280w, http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_540"
                       ".jpg 540w, http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90"
                       "/tumblr_nshp8oVOnV1rg0s9xo1_250.jpg 250w",
                alt="Sonic the Hedgehog and friends",
                cls="image", loading="lazy",
                sizes="(max-width: 540px) 100vh, 540px",
            ), cls="image-container"),

            dominate.tags.figcaption(
                "I'm living my best life on earth.",
                cls="image-caption"
            ),

            cls="image-block"
        ),

        cls="post-body"
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
            src="http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_250.gif",
            srcset="http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/"
                   "tumblr_nshp8oVOnV1rg0s9xo1_250.gif 250w",
            cls="image", loading="lazy",
            sizes="(max-width: 540px) 100vh, 540px",
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
            src="http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg",
            srcset="http://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/"
                   "tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg 1280w",
            cls="image", loading="lazy",
            sizes="(max-width: 540px) 100vh, 540px",
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
            src="https://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_500.gif",
            srcset="https://69.media.tumblr.com/b06fe71cc4ab47e93749df060ff54a90/"
                   "tumblr_nshp8oVOnV1rg0s9xo1_500.gif 500w",
            cls="image", loading="lazy",
            sizes="(max-width: 540px) 100vh, 540px",
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
    )],

    format_constructor(
        dominate.tags.img(
            src="https://64.media.tumblr.com/s400x600/blahblahblah.gifv",
            srcset="https://64.media.tumblr.com/s400x600/blahblahblah.gifv 357w, "
                   "https://64.media.tumblr.com/s250x400/blahblahblah.gifv 250w",
            cls="image", loading="lazy",
            sizes="(max-width: 540px) 100vh, 540px",
            alt="image",
        ),

        dominate.tags.div(
            dominate.tags.a(
                "From ",
                dominate.tags.b(
                    "example-blog",
                ),
                href="https://example-blog.tumblr.com/post/1234567890/example-gif-post",
            ),
            cls="post-attribution"
        )
    ),
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
    )],

    format_constructor(
        dominate.tags.img(
            src="https://64.media.tumblr.com/0655920c23ca997bf6145c32bda00cc5/14ab5a4c91df05c8-c8/s500x750/23f1c831d79fb51b56bbd52ae7d8c03336fd6f25.gifv",
            srcset="https://64.media.tumblr.com/0655920c23ca997bf6145c32bda00cc5/14ab5a4c91df05c8-c8/s500x750"
                   "/23f1c831d79fb51b56bbd52ae7d8c03336fd6f25.gifv 500w",
            cls="image", loading="lazy",
            sizes="(max-width: 540px) 100vh, 540px",
            alt="image",
        ),

        dominate.tags.div(
            dominate.tags.a(
                "davidragifs.com",
                href="https://davidragifs.com",
            ),
            cls="link-attribution"
        )
    ),
)

image_block_with_app_attribution = (
    [
        {
            "type": "image",
            "media": [
                {
                    "mediaKey": "23ca9c69bda0020ca4c91df05c8-c8",
                    "type": "image/jpeg",
                    "width": 779,
                    "height": 723,
                    "url": "https://example.com/image/s1280x1920.jpg",
                    "hasOriginalDimensions": True
                },

                {
                    "mediaKey": "269bda0020ca4c91df05c8a00f5c8-c8",
                    "type": "image/jpeg",
                    "width": 640,
                    "height": 594,
                    "url": "https://example.com/image/s640x960.jpg",
                },
            ]
        },

        {
            "type": "text",
            "text": "Check out my commission from author! Please follow them here https://twitter.com/example",
            "formatting": [
                {
                    "type": "link",
                    "start": 61,
                    "end": 88,
                    "url": "https://twitter.com/example"
                }
            ]
        },

        {
            "type": "image",
            "media": [
                {
                    "mediaKey": "0655920c23ca997bf6145c32bda00cc5:14ab5a4c91df05c8-c8",
                    "type": "image/jpeg",
                    "width": 1096,
                    "height": 1428,
                    "url": "https://example.com/image/s1280x1920/2.jpg",
                    "hasOriginalDimensions": True
                },
            ],
            "attribution": {
                "type": "app",
                "appName": "Twitter",
                "url": "https://twitter.com/example/status/1234567",
                "displayText": "View on Twitter"

            },
            "colors": {
                "c0": "ff2ffe",
                "c1": "424242",
                "c2": "083808",
                "c3": "b5b6b7",
            },
        }
    ],
    [
        objects.image.ImageBlock(
            media=[
                objects.media_objects.MediaObject(
                    url='https://example.com/image/s1280x1920.jpg',
                    type='image/jpeg',
                    width=779,
                    height=723,
                    has_original_dimensions=True
                ),
                objects.media_objects.MediaObject(
                    url='https://example.com/image/s640x960.jpg',
                    type='image/jpeg',
                    width=640,
                    height=594,
                ),
            ],
        ),

        objects.text_block.TextBlock(
            text="Check out my commission from author! Please follow them here https://twitter.com/example",
            inline_formatting= [
                objects.inline.Link(
                    type=objects.inline.FMTTypes.LINK,
                    start=61,
                    end=88,
                    url="https://twitter.com/example"
                )
            ]
        ),

        objects.image.ImageBlock(
            media=[
                objects.media_objects.MediaObject(
                    url='https://example.com/image/s1280x1920/2.jpg',
                    type='image/jpeg',
                    width=1096,
                    height=1428,
                    has_original_dimensions=True,
                ),
            ],

            colors=["ff2ffe", "424242", "083808", "b5b6b7"],

            attribution=objects.attribution.AppAttribution(
                url="https://twitter.com/example/status/1234567",
                app_name="Twitter",
                display_text="View on Twitter"
            ),
        ),
    ],

    dominate.tags.div(
        dominate.tags.figure(dominate.tags.div(
            dominate.tags.img(
                src="https://example.com/image/s1280x1920.jpg",
                srcset="https://example.com/image/s1280x1920.jpg "
                       "779w, https://example.com/image/s640x960.jpg 640w",
                cls="image", loading="lazy",
                sizes="(max-width: 540px) 100vh, 540px",
                alt="image",
            ), cls="image-container"),
            cls="image-block"
        ),

        dominate.tags.p(
            dominate.tags.span(
                "Check out my commission from author! Please follow them here ",
                dominate.tags.a("https://twitter.com/example", href="https://twitter.com/example", cls="inline-link"),
                cls="inline-formatted-content",
            ),
            cls="text-block",
        ),

        dominate.tags.figure(
            dominate.tags.div(
                dominate.tags.img(
                    src="https://example.com/image/s1280x1920/2.jpg",
                    srcset="https://example.com/image/s1280x1920/2.jpg 1096w",
                    cls="image", loading="lazy",
                    sizes="(max-width: 540px) 100vh, 540px",
                    alt="image"
                ),

                dominate.tags.div(
                    dominate.tags.a(
                        "View on ",
                        dominate.tags.b(
                            "Twitter"
                        ),
                        href="https://twitter.com/example/status/1234567"
                    ),
                    cls="post-attribution"
                ),

                cls="image-container"
            ),
            cls="image-block"
        ),


        cls="post-body"
    )

)


image_block_with_replaced_link = (
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
                src="http://example.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg",
                srcset="http://example.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_1280.jpg "
                       "1280w, http://example.com/b06fe71cc4ab47e93749df060ff54a90/tumblr_nshp8oVOnV1rg0s9xo1_540"
                       ".jpg 540w, http://example.com/b06fe71cc4ab47e93749df060ff54a90"
                       "/tumblr_nshp8oVOnV1rg0s9xo1_250.jpg 250w",
                alt="Sonic the Hedgehog and friends",
                cls="image", loading="lazy",
                sizes="(max-width: 540px) 100vh, 540px",
            ), cls="image-container"),

            dominate.tags.figcaption(
                "I'm living my best life on earth.",
                cls="image-caption"
            ),

            cls="image-block"
        ),

        cls="post-body"
    )
)


skip_cropped_image_block_test = (
    [
        {
            "type": "image",
            "media": [
                {
                    "type": "image/jpeg",
                    "url": "https://example.com/image/s1280x1920.jpg",
                    "width": 1280,
                    "height": 1920
                },
                {
                    "type": "image/jpeg",
                    "url": "https://example.com/image/s640x460.jpg",
                    "width": 640.0,
                    "height": 460.0,
                    "cropped": True,
                },
                {
                    "type": "image/jpeg",
                    "url": "https://example.com/image/s512x512.jpg",
                    "width": 512,
                    "height": 512,
                    "cropped": True,
                },

                {
                    "type": "image/jpeg",
                    "url": "https://example.com/image/s320x480.jpg",
                    "width": 320,
                    "height": 480,
                    "hasOriginalDimensions": True
                }
            ],
        }
    ],

    dominate.tags.div(
        dominate.tags.figure(dominate.tags.div(
            dominate.tags.img(
                src="https://example.com/image/s320x480.jpg",
                srcset="https://example.com/image/s1280x1920.jpg 1280w, https://example.com/image/s320x480.jpg 320w",
                alt="image",
                cls="image", loading="lazy",
                sizes="(max-width: 540px) 100vh, 540px",
            ), cls="image-container"),

            cls="image-block"
        ),

        cls="post-body"
    )
)
