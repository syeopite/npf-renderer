import dominate.tags

from npf_renderer.objects import layouts, attribution

content_list = [
    {"type": "text", "text": "Hi there"},
    {"type": "image", "media": [{"url": "https://example.com/example-image-1.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-2.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-3.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-4.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-5.png"}]}
]

basic_rows_layout_example = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [1, 2]},
                    {"blocks": [3]},
                ]
            }
        ]
    },
    [
        layouts.Rows(
            rows=[
                layouts.RowLayout(
                    [1, 2]
                ),
                layouts.RowLayout(
                    [3, ]
                )
            ]
        )
    ],
    (
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.figure(
                    dominate.tags.div(
                        dominate.tags.img(
                            srcset="https://example.com/example-image-1.png 540w",
                            cls="image",
                            sizes="(max-width: 540px) 50vh, 270px",
                            alt="image",
                        ),
                        cls="image-container"
                    ),
                    cls="image-block"
                ),

                dominate.tags.figure(
                    dominate.tags.div(
                        dominate.tags.img(
                            srcset="https://example.com/example-image-2.png 540w",
                            cls="image",
                            sizes="(max-width: 540px) 50vh, 270px",
                            alt="image",
                        ),
                        cls="image-container"
                    ),
                    cls="image-block"
                ),

                cls="layout-row"
            ),

            dominate.tags.div(
                dominate.tags.figure(
                    dominate.tags.div(
                        dominate.tags.img(
                            srcset="https://example.com/example-image-3.png 540w",
                            cls="image",
                            sizes="(max-width: 540px) 100vh, 540px",
                            alt="image",
                        ),
                        cls="image-container"
                    ),
                    cls="image-block"
                ),

                cls="layout-row"
            ),

            cls="post")
    )
)

basic_rows_layout_with_truncate_example = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [1, 2, 3]},
                    {"blocks": [4, 5]},
                ],

                "truncate_after": 3,
            }
        ]
    },
    [
        layouts.Rows(
            rows=[
                layouts.RowLayout(
                    [1, 2, 3]
                ),
                layouts.RowLayout(
                    [4, 5]
                )
            ],

            truncate_after=3
        )
    ]
)

rows_with_carousel_and_weighted = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [1, 2, 3], "mode": {"type": "carousel"}},
                    {"blocks": [4, 5]},
                ],
            }
        ]
    },
    [
        layouts.Rows(
            rows=[
                layouts.RowLayout(
                    [1, 2, 3],
                    display_mode=layouts.DisplayMode.CAROUSEL
                ),
                layouts.RowLayout(
                    [4, 5]
                )
            ],
        )
    ]
)

layouts_with_ask_section = (
    {
        "layouts": [
            {
                "type": "ask",
                "blocks": [0, 1, 2],
                "attribution": {
                    "type": "blog",
                    "url": "https://example.tumblr.com",
                    "blog": {
                        "name": "example",
                        "url": "https://example.tumblr.com",
                        "uuid": "t:SN32hxaWHi312_32_df"
                    }
                }
            },
            {
                "type": "rows",
                "display": [
                    {"blocks": [0]},
                    {"blocks": [1]},
                    {"blocks": [2]},

                    {"blocks": [3]},
                    {"blocks": [4, 5]},
                ],

                "truncate_after": 3
            }
        ]
    },

    [
        layouts.AskLayout(
            ranges=[0, 1, 2],
            attribution=attribution.BlogAttribution(
                name="example",
                url="https://example.tumblr.com",
                uuid="t:SN32hxaWHi312_32_df"
            )

        ),

        layouts.Rows(
            rows=[
                layouts.RowLayout(
                    [3],
                ),
                layouts.RowLayout(
                    [4, 5]
                )
            ],

            truncate_after=3
        )
    ]
)

layouts_with_anon_ask_section = (
    {
        "layouts": [
            {
                "type": "ask",
                "blocks": [0],
                "attribution": None
            },
            {
                "type": "rows",
                "display": [
                    {"blocks": [0]},
                    {"blocks": [1, 2, 3]},
                    {"blocks": [4, 5]},
                ],
            }
        ]
    },

    [
        layouts.AskLayout(
            ranges=[0]

        ),

        layouts.Rows(
            rows=[
                layouts.RowLayout(
                    [1, 2, 3],
                ),
                layouts.RowLayout(
                    [4, 5]
                )
            ],
        )
    ]
)
