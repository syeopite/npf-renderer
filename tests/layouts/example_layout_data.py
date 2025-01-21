import dominate.tags

from npf_renderer.objects import layouts, attribution

content_list = [
    {"type": "text", "text": "Hi there"},
    # Uses default width and height of 540 x 405
    {"type": "image", "media": [{"url": "https://example.com/example-image-1.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-2.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-3.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-4.png"}]},
    {"type": "image", "media": [{"url": "https://example.com/example-image-5.png"}]},
]


def generate_image_block_html(index, siblings):
    inner = (
        dominate.tags.div(
            dominate.tags.img(
                src=f"https://example.com/example-image-{index}.png",
                srcset=f"https://example.com/example-image-{index}.png 540w",
                cls="image",
                loading="lazy",
                sizes=f"(max-width: 540px) {round(100 / siblings)}vh, {round(540 / siblings)}px",
                alt="image",
            ),
            cls="image-container",
            style="aspect-ratio: 1.3333;",
        ),
    )

    return dominate.tags.figure(inner, cls="image-block")


basic_rows_layout_example = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [1, 2]},
                    {"blocks": [3]},
                ],
            }
        ]
    },
    [
        layouts.Rows(
            rows=[
                layouts.RowLayout([1, 2]),
                layouts.RowLayout(
                    [
                        3,
                    ]
                ),
            ]
        )
    ],
    (
        dominate.tags.div(
            dominate.tags.div(generate_image_block_html(1, 2), generate_image_block_html(2, 2), cls="layout-row"),
            dominate.tags.div(generate_image_block_html(3, 1), cls="layout-row"),
            cls="post-body",
        )
    ),
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
    [layouts.Rows(rows=[layouts.RowLayout([1, 2, 3]), layouts.RowLayout([4, 5])], truncate_after=3)],
    (
        dominate.tags.div(
            dominate.tags.div(
                generate_image_block_html(1, 3),
                generate_image_block_html(2, 3),
                generate_image_block_html(3, 3),
                cls="layout-row",
            ),
            dominate.tags.details(
                dominate.tags.summary("Read more"),
                dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
                cls="layout-truncated",
            ),
            cls="post-body",
        )
    ),
)


basic_rows_layout_with_truncate_example_disabled_truncation = (
    basic_rows_layout_with_truncate_example[0],
    (
        dominate.tags.div(
            dominate.tags.div(
                generate_image_block_html(1, 3),
                generate_image_block_html(2, 3),
                generate_image_block_html(3, 3),
                cls="layout-row",
            ),
            dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
            cls="post-body",
        )
    ),
)


basic_rows_layout_with_camel_case_truncate_example = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [1, 2, 3]},
                    {"blocks": [4, 5]},
                ],
                "truncateAfter": 3,
            }
        ]
    },
    basic_rows_layout_with_truncate_example[1],
)


basic_rows_layout_with_truncate_at_start_example = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [1, 2, 3]},
                    {"blocks": [4, 5]},
                ],
                "truncate_after": -1,
            }
        ]
    },
    [layouts.Rows(rows=[layouts.RowLayout([1, 2, 3]), layouts.RowLayout([4, 5])], truncate_after=-1)],
    (
        dominate.tags.div(
            dominate.tags.details(
                dominate.tags.summary("Read more"),
                dominate.tags.div(
                    generate_image_block_html(1, 3),
                    generate_image_block_html(2, 3),
                    generate_image_block_html(3, 3),
                    cls="layout-row",
                ),
                dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
                cls="layout-truncated",
            ),
            cls="post-body",
        )
    ),
)

basic_rows_layout_with_truncate_at_start_example_disabled_truncation = (
    basic_rows_layout_with_truncate_at_start_example[0],
    (
        dominate.tags.div(
            dominate.tags.div(
                generate_image_block_html(1, 3),
                generate_image_block_html(2, 3),
                generate_image_block_html(3, 3),
                cls="layout-row",
            ),
            dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
            cls="post-body",
        )
    ),
)


rows_layout_truncate_after_0th_block = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [0]},
                    {"blocks": [1, 2, 3]},
                    {"blocks": [4, 5]},
                ],
                "truncate_after": 0,
            }
        ]
    },
    [
        layouts.Rows(
            rows=[layouts.RowLayout([0]), layouts.RowLayout([1, 2, 3]), layouts.RowLayout([4, 5])], truncate_after=0
        )
    ],
    (
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.p("Hi there", cls="text-block"),
                cls="layout-row",
            ),
            dominate.tags.details(
                dominate.tags.summary("Read more"),
                dominate.tags.div(
                    generate_image_block_html(1, 3),
                    generate_image_block_html(2, 3),
                    generate_image_block_html(3, 3),
                    cls="layout-row",
                ),
                dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
                cls="layout-truncated",
            ),
            cls="post-body",
        )
    ),
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
            rows=[layouts.RowLayout([1, 2, 3], display_mode=layouts.DisplayMode.CAROUSEL), layouts.RowLayout([4, 5])],
        )
    ],
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
                    "blog": {"name": "example", "url": "https://example.tumblr.com", "uuid": "t:SN32hxaWHi312_32_df"},
                },
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
            },
        ]
    },
    [
        layouts.AskLayout(
            ranges=[0, 1, 2],
            attribution=attribution.BlogAttribution(
                name="example", url="https://example.tumblr.com", uuid="t:SN32hxaWHi312_32_df"
            ),
        ),
        layouts.Rows(
            rows=[
                layouts.RowLayout(
                    [3],
                ),
                layouts.RowLayout([4, 5]),
            ],
        ),
    ],
    dominate.tags.div(
        # Ask
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.div(
                        dominate.tags.p(
                            dominate.util.raw(
                                dominate.tags.a(
                                    dominate.tags.strong("example", cls="asker-name"),
                                    href="https://example.tumblr.com/",
                                    cls="asker-attribution",
                                ).render(pretty=False)
                            ),
                            " asked:",
                            cls="asker",
                        ),
                        cls="ask-header",
                    ),
                    dominate.tags.div(
                        dominate.tags.p("Hi there", cls="text-block"),
                        generate_image_block_html(1, 1),
                        generate_image_block_html(2, 1),
                        cls="ask-content",
                    ),
                    cls="ask-body",
                ),
                cls="ask",
            ),
            cls="layout-ask",
        ),
        dominate.tags.div(generate_image_block_html(3, 1), cls="layout-row"),
        dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
        cls="post-body",
    ),
)


layouts_with_ask_section_and_truncation = (
    {
        "layouts": [
            {
                "type": "ask",
                "blocks": [0, 1, 2],
                "attribution": {
                    "type": "blog",
                    "url": "https://example.tumblr.com",
                    "blog": {"name": "example", "url": "https://example.tumblr.com", "uuid": "t:SN32hxaWHi312_32_df"},
                },
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
                "truncate_after": 3,
            },
        ]
    },
    [
        layouts.AskLayout(
            ranges=[0, 1, 2],
            attribution=attribution.BlogAttribution(
                name="example", url="https://example.tumblr.com", uuid="t:SN32hxaWHi312_32_df"
            ),
        ),
        layouts.Rows(
            rows=[
                layouts.RowLayout(
                    [3],
                ),
                layouts.RowLayout([4, 5]),
            ],
            truncate_after=3,
        ),
    ],
    dominate.tags.div(
        # Ask
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.div(
                        dominate.tags.p(
                            dominate.util.raw(
                                dominate.tags.a(
                                    dominate.tags.strong("example", cls="asker-name"),
                                    href="https://example.tumblr.com/",
                                    cls="asker-attribution",
                                ).render(pretty=False),
                            ),
                            " asked:",
                            cls="asker",
                        ),
                        cls="ask-header",
                    ),
                    dominate.tags.div(
                        dominate.tags.p("Hi there", cls="text-block"),
                        generate_image_block_html(1, 1),
                        generate_image_block_html(2, 1),
                        cls="ask-content",
                    ),
                    cls="ask-body",
                ),
                cls="ask",
            ),
            cls="layout-ask",
        ),
        dominate.tags.div(generate_image_block_html(3, 1), cls="layout-row"),
        dominate.tags.details(
            dominate.tags.summary("Read more"),
            dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
            cls="layout-truncated",
        ),
        cls="post-body",
    ),
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
                    "blog": {"name": "example", "url": "https://example.tumblr.com", "uuid": "t:SN32hxaWHi312_32_df"},
                },
            }
        ]
    },
    [
        layouts.AskLayout(
            ranges=[0, 1, 2],
            attribution=attribution.BlogAttribution(
                name="example", url="https://example.tumblr.com", uuid="t:SN32hxaWHi312_32_df"
            ),
        ),
    ],
    dominate.tags.div(
        # Ask
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.div(
                        dominate.tags.p(
                            dominate.util.raw(
                                dominate.tags.a(
                                    dominate.tags.strong("example", cls="asker-name"),
                                    href="https://example.tumblr.com/",
                                    cls="asker-attribution",
                                ).render(pretty=False)
                            ),
                            " asked:",
                            cls="asker",
                        ),
                        cls="ask-header",
                    ),
                    dominate.tags.div(
                        dominate.tags.p("Hi there", cls="text-block"),
                        generate_image_block_html(1, 1),
                        generate_image_block_html(2, 1),
                        cls="ask-content",
                    ),
                    cls="ask-body",
                ),
                cls="ask",
            ),
            cls="layout-ask",
        ),
        dominate.tags.div(generate_image_block_html(3, 1), cls="layout-row"),
        dominate.tags.div(generate_image_block_html(4, 1), cls="layout-row"),
        dominate.tags.div(generate_image_block_html(5, 1), cls="layout-row"),
        cls="post-body",
    ),
)


layouts_with_anon_ask_section = (
    {
        "layouts": [
            {"type": "ask", "blocks": [0], "attribution": None},
            {
                "type": "rows",
                "display": [
                    {"blocks": [0]},
                    {"blocks": [1, 2, 3]},
                    {"blocks": [4, 5]},
                ],
            },
        ]
    },
    [
        layouts.AskLayout(ranges=[0]),
        layouts.Rows(
            rows=[
                layouts.RowLayout(
                    [1, 2, 3],
                ),
                layouts.RowLayout([4, 5]),
            ],
        ),
    ],
    dominate.tags.div(
        # Ask
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.div(
                        dominate.tags.p(
                            dominate.util.raw(dominate.tags.strong("Anonymous", cls="asker-name").render(pretty=False)),
                            " asked:",
                            cls="asker",
                        ),
                        cls="ask-header",
                    ),
                    dominate.tags.div(dominate.tags.p("Hi there", cls="text-block"), cls="ask-content"),
                    cls="ask-body",
                ),
                dominate.tags.img(
                    src="https://assets.tumblr.com/images/anonymous_avatar_96.gif",
                    loading="lazy",
                    cls="avatar asker-avatar image",
                ),
                cls="ask",
            ),
            cls="layout-ask",
        ),
        dominate.tags.div(
            generate_image_block_html(1, 3),
            generate_image_block_html(2, 3),
            generate_image_block_html(3, 3),
            cls="layout-row",
        ),
        dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
        cls="post-body",
    ),
)


# Because we merge list subtypes blocks together
# We need to pad the amount of total blocks within the formatter
# as to successfully arrange blocks in accordance to the layout given
# by Tumblr

with_list_content_list = (
    content_list[0],
    {"type": "text", "text": "item 1", "subtype": "unordered-list-item"},
    {"type": "text", "text": "item 2", "subtype": "unordered-list-item"},
    {"type": "text", "text": "item 3", "subtype": "unordered-list-item"},
    {"type": "text", "text": "item 4", "subtype": "unordered-list-item"},
    *content_list[1:],
)


layouts_in_content_with_lists = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [0]},
                    {"blocks": [1]},
                    {"blocks": [2]},
                    {"blocks": [3]},
                    {"blocks": [4]},
                    {"blocks": [5]},
                    {"blocks": [6, 7]},
                    {"blocks": [8, 9]},
                ],
            }
        ]
    },
    [
        layouts.Rows(
            rows=[
                layouts.RowLayout([0]),
                layouts.RowLayout([1]),
                layouts.RowLayout([2]),
                layouts.RowLayout([3]),
                layouts.RowLayout([4]),
                layouts.RowLayout([5]),
                layouts.RowLayout([6, 7]),
                layouts.RowLayout([8, 9]),
            ],
        )
    ],
    dominate.tags.div(
        dominate.tags.div(dominate.tags.p("Hi there", cls="text-block"), cls="layout-row"),
        dominate.tags.div(
            dominate.tags.ul(
                dominate.tags.li("item 1", cls="text-block unordered-list-item"),
                dominate.tags.li("item 2", cls="text-block unordered-list-item"),
                dominate.tags.li("item 3", cls="text-block unordered-list-item"),
                dominate.tags.li("item 4", cls="text-block unordered-list-item"),
                cls="unordered-list",
            ),
            cls="layout-row",
        ),
        dominate.tags.div(generate_image_block_html(1, 1), cls="layout-row"),
        dominate.tags.div(generate_image_block_html(2, 2), generate_image_block_html(3, 2), cls="layout-row"),
        dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
        cls="post-body",
    ),
)


# Because nested NPF text blocks are grouped together, we need to pad the render instructions
# in order to account for the missing blocks.


with_nested_blocks_content_list = (
    {"type": "text", "subtype": "indented", "text": "1: blockquote, not nested"},
    {"type": "text", "subtype": "indented", "text": "2: blockquote, nested", "indent_level": 1},
    {"type": "text", "subtype": "unordered-list-item", "text": "3: nested in two blockquotes", "indent_level": 2},
    {
        "type": "text",
        "subtype": "ordered-list-item",
        "text": "4: nested in two blockquotes and a list",
        "indent_level": 3,
    },
    {"type": "text", "subtype": "unordered-list-item", "text": "3: back to level 3, double nesting", "indent_level": 2},
    {
        "type": "text",
        "subtype": "indented",
        "text": "1: back to level 1, no nesting",
    },
)


with_nested_blocks_layout_list = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [0]},
                    {"blocks": [1]},
                    {"blocks": [2]},
                    {"blocks": [3]},
                    {"blocks": [4]},
                    {"blocks": [5]},
                ],
            }
        ]
    },
    [
        layouts.Rows(
            rows=[
                layouts.RowLayout([0]),
                layouts.RowLayout([1]),
                layouts.RowLayout([2]),
                layouts.RowLayout([3]),
                layouts.RowLayout([4]),
                layouts.RowLayout([5]),
            ],
        )
    ],
    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.blockquote(
                "1: blockquote, not nested",
                dominate.tags.blockquote(
                    "2: blockquote, nested",
                    dominate.tags.ul(
                        dominate.tags.li(
                            "3: nested in two blockquotes",
                            dominate.tags.ol(
                                dominate.tags.li(
                                    "4: nested in two blockquotes and a list", cls="text-block ordered-list-item"
                                ),
                                cls="ordered-list",
                            ),
                            cls="text-block unordered-list-item",
                        ),
                        dominate.tags.li("3: back to level 3, double nesting", cls="text-block unordered-list-item"),
                        cls="unordered-list",
                    ),
                    cls="text-block indented",
                ),
                cls="text-block indented",
            ),
            cls="layout-row",
        ),
        dominate.tags.div(
            dominate.tags.blockquote("1: back to level 1, no nesting", cls="text-block indented"), cls="layout-row"
        ),
        cls="post-body",
    ),
)


with_nested_list_blocks_content_list = (
    {"type": "text", "subtype": "heading1", "text": "Sward's Shopping List"},
    {
        "type": "text",
        "subtype": "ordered-list-item",
        "text": "First level: Fruit",
    },
    {
        "type": "text",
        "subtype": "unordered-list-item",
        "text": "Second level: Apples",
        "indent_level": 1,
    },
    {
        "type": "text",
        "subtype": "ordered-list-item",
        "text": "Third Level: Green",
        "indent_level": 2,
    },
    {
        "type": "text",
        "subtype": "unordered-list-item",
        "text": "Second level: Pears",
        "indent_level": 1,
    },
    {
        "type": "text",
        "subtype": "ordered-list-item",
        "text": "First level: Pears",
    },
)


with_nested_list_blocks_layout_list = (
    {
        "layouts": [
            {
                "type": "rows",
                "display": [
                    {"blocks": [0]},
                    {"blocks": [1]},
                    {"blocks": [2]},
                    {"blocks": [3]},
                    {"blocks": [4]},
                    {"blocks": [5]},
                ],
            }
        ]
    },
    [
        layouts.Rows(
            rows=[
                layouts.RowLayout([0]),
                layouts.RowLayout([1]),
                layouts.RowLayout([2]),
                layouts.RowLayout([3]),
                layouts.RowLayout([4]),
                layouts.RowLayout([5]),
            ],
        )
    ],
    dominate.tags.div(
        dominate.tags.div(dominate.tags.h1("Sward's Shopping List", cls="text-block heading1"), cls="layout-row"),
        dominate.tags.div(
            dominate.tags.ol(
                dominate.tags.li(
                    "First level: Fruit",
                    dominate.tags.ul(
                        dominate.tags.li(
                            "Second level: Apples",
                            dominate.tags.ol(
                                dominate.tags.li("Third Level: Green", cls="text-block ordered-list-item"),
                                cls="ordered-list",
                            ),
                            cls="text-block unordered-list-item",
                        ),
                        dominate.tags.li("Second level: Pears", cls="text-block unordered-list-item"),
                        cls="unordered-list",
                    ),
                    cls="text-block ordered-list-item",
                ),
                dominate.tags.li("First level: Pears", cls="text-block ordered-list-item"),
                cls="ordered-list",
            ),
            cls="layout-row",
        ),
        cls="post-body",
    ),
)
