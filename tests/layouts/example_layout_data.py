import dominate.tags

from npf_renderer.objects import layouts, attribution

content_list = [
    {"type": "text", "text": "Hi there"},
    {"type": "image", "media": [{"url": "https://example.com/example-image-1.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-2.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-3.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-4.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-5.png"}]},
]


def generate_image_block_html(index, siblings):
    return dominate.tags.figure(
        dominate.tags.div(
            dominate.tags.img(
                srcset=f"https://example.com/example-image-{index}.png 540w",
                cls="image", loading="lazy",
                sizes=f"(max-width: 540px) {round(100 / siblings)}vh, {round(540 / siblings)}px",
                alt="image",
            ),
            cls="image-container"
        ),
        cls="image-block"
    ),


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
                generate_image_block_html(1, 2),
                generate_image_block_html(2, 2),
                cls="layout-row"
            ),

            dominate.tags.div(
                generate_image_block_html(3, 1),
                cls="layout-row"
            ),

            cls="post-body")
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
    ],

    dominate.tags.div(
        # Ask
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.div(
                        dominate.tags.p(
                            dominate.tags.a(
                                dominate.tags.strong("example", cls="asker-name"),
                                href="https://example.tumblr.com/",
                                cls="asker-attribution"
                            ),
                            " asked:",
                            cls="asker"
                        ),
                        cls="ask-header"
                    ),

                    dominate.tags.div(
                        dominate.tags.p("Hi there", cls="text-block"),
                        generate_image_block_html(1, 1),
                        generate_image_block_html(2, 1),
                        cls="ask-content"
                    ),

                    cls="ask-body"
                ),

                cls="ask"
            ),
            cls="layout-ask"
        ),

        dominate.tags.div(
            generate_image_block_html(3, 1),
            cls="layout-row"
        ),

        dominate.tags.div(
            generate_image_block_html(4, 2),
            generate_image_block_html(5, 2),
            cls="layout-row"
        ),

        cls="post-body"
    )
)

layouts_with_only_ask_section = (
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
    ],

    dominate.tags.div(
        # Ask
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.div(
                        dominate.tags.p(
                            dominate.tags.a(
                                dominate.tags.strong("example", cls="asker-name"),
                                href="https://example.tumblr.com/",
                                cls="asker-attribution"
                            ),
                            " asked:",
                            cls="asker"
                        ),
                        cls="ask-header"
                    ),

                    dominate.tags.div(
                        dominate.tags.p("Hi there", cls="text-block"),
                        generate_image_block_html(1, 1),
                        generate_image_block_html(2, 1),
                        cls="ask-content"
                    ),

                    cls="ask-body"
                ),

                cls="ask"
            ),
            cls="layout-ask"
        ),

        dominate.tags.div(
            generate_image_block_html(3, 1),
            cls="layout-row"
        ),

        dominate.tags.div(
            generate_image_block_html(4, 1),
            cls="layout-row"
        ),

        dominate.tags.div(
            generate_image_block_html(5, 1),
            cls="layout-row"
        ),

        cls="post-body"
    )

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
    ],

    dominate.tags.div(
        # Ask
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.div(
                        dominate.tags.p(
                            dominate.tags.strong("Anonymous", cls="asker-name"),
                            " asked:",
                            cls="asker"
                        ),
                        cls="ask-header"
                    ),

                    dominate.tags.div(
                        dominate.tags.p("Hi there", cls="text-block"),
                        cls="ask-content"
                    ),
                    cls="ask-body"
                ),

                dominate.tags.img(
                    src="https://assets.tumblr.com/images/anonymous_avatar_96.gif",
                    loading="lazy",
                    cls="avatar asker-avatar image"
                ),
                cls="ask"
            ),
            cls="layout-ask"
        ),

        dominate.tags.div(
            generate_image_block_html(1, 3),
            generate_image_block_html(2, 3),
            generate_image_block_html(3, 3),
            cls="layout-row"
        ),

        dominate.tags.div(
            generate_image_block_html(4, 2),
            generate_image_block_html(5, 2),
            cls="layout-row"
        ),

        cls="post-body"
    )

)
