from dominate import tags

from npf_renderer import objects

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
    ]
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
    ]
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
    ]
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
    ]
)


