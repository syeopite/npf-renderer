from dominate import tags

from npf_renderer import objects


standard_test = (
    {
        "content": [
            {
                "type": "text",
                "text": "some small text",
                "formatting": [{"start": 5, "end": 10, "type": "small"}],
            },
        ]
    },
    [
        objects.text_block.TextBlock(
            text="some small text",
            inline_formatting=[objects.inline.Standard(type=objects.inline.FMTTypes.SMALL, start=5, end=10)],
        )
    ],
    tags.div(
        tags.p(
            tags.span("some ", tags.small("small", cls="inline-small"), " text", cls="inline-formatted-content"),
            cls="text-block",
        ),
        cls="post",
    ),
)

#     {"content": }, "12345"

link_test = (
    {
        "content": [
            {
                "type": "text",
                "text": "Found this link for you",
                "formatting": [
                    {
                        "start": 6,
                        "end": 10,
                        "type": "link",
                        "url": "https://www.nasa.gov",
                    }
                ],
            }
        ]
    },
    [
        objects.text_block.TextBlock(
            text="Found this link for you",
            inline_formatting=[
                objects.inline.Link(
                    type=objects.inline.FMTTypes.LINK,
                    start=6,
                    end=10,
                    url="https://www.nasa.gov",
                )
            ],
        )
    ],
    tags.div(
        tags.p(
            tags.span(
                "Found ",
                tags.a("this", href="https://www.nasa.gov", cls="inline-link"),
                " link for you",
                cls="inline-formatted-content",
            ),
            cls="text-block",
        ),
        cls="post",
    ),
)
mention_test = (
    {
        "content": [
            {
                "type": "text",
                "text": "Shout out to @david",
                "formatting": [
                    {
                        "start": 13,
                        "end": 19,
                        "type": "mention",
                        "blog": {
                            "uuid": "t:123456abcdf",
                            "name": "david",
                            "url": "https://davidslog.com/",
                        },
                    }
                ],
            }
        ]
    },
    [
        objects.text_block.TextBlock(
            text="Shout out to @david",
            inline_formatting=[
                objects.inline.Mention(
                    type=objects.inline.FMTTypes.MENTION,
                    start=13,
                    end=19,
                    blog_uuid="t:123456abcdf",
                    blog_name="david",
                    blog_url="https://davidslog.com/",
                )
            ],
        )
    ],
    tags.div(
        tags.p(
            tags.span(
                "Shout out to ",
                tags.a("@david", cls="inline-mention", href="https://davidslog.com/"),
                cls="inline-formatted-content",
            ),
            cls="text-block",
        ),
        cls="post",
    ),
)

color_test = (
    {
        "content": [
            {
                "type": "text",
                "text": "Celebrate Pride Month",
                "formatting": [{"start": 10, "end": 15, "type": "color", "hex": "#ff492f"}],
            }
        ]
    },
    [
        objects.text_block.TextBlock(
            text="Celebrate Pride Month",
            inline_formatting=[
                objects.inline.Color(type=objects.inline.FMTTypes.COLOR, start=10, end=15, hex="#ff492f")
            ],
        )
    ],
    tags.div(
        tags.p(
            tags.span(
                "Celebrate ",
                tags.span("Pride", cls="inline-color", style="color: #ff492f;"),
                " Month",
                cls="inline-formatted-content",
            ),
            cls="text-block",
        ),
        cls="post",
    ),
)

test_overlapping = (
    {
        "content": [
            {
                "type": "text",
                "text": "supercalifragilisticexpialidocious",
                "formatting": [
                    {"start": 0, "end": 20, "type": "bold"},
                    {"start": 9, "end": 34, "type": "italic"},
                ],
            }
        ]
    },
    [
        objects.text_block.TextBlock(
            text="supercalifragilisticexpialidocious",
            inline_formatting=[
                objects.inline.Standard(
                    type=objects.inline.FMTTypes.BOLD,
                    start=0,
                    end=20,
                ),
                objects.inline.Standard(
                    type=objects.inline.FMTTypes.ITALIC,
                    start=9,
                    end=34,
                ),
            ],
        ),
    ],
    tags.div(
        tags.p(
            tags.span(
                tags.b(
                    "supercali",
                    tags.i("fragilistic", cls="inline-italics"),
                    cls="inline-bold",
                ),
                tags.i("expialidocious", cls="inline-italics"),
                cls="inline-formatted-content",
            ),
            cls="text-block",
        ),
        cls="post",
    ),
)

test_total_overlapping = (
    {
        "content": [
            {
                "type": "text",
                "text": "supercalifragilisticexpialidocious",
                "formatting": [
                    {"start": 0, "end": 34, "type": "bold"},
                    {"start": 0, "end": 34, "type": "italic"},
                    {"start": 0, "end": 34, "type": "small"},
                    {"start": 0, "end": 34, "type": "strikethrough"},
                    {"start": 0, "end": 34, "type": "link",
                     "url": "https://en.wiktionary.org/wiki/supercalifragilisticexpialidocious"},
                ],
            }
        ]
    },
    [
        objects.text_block.TextBlock(
            text="supercalifragilisticexpialidocious",
            inline_formatting=[
                objects.inline.TotalOverlaps(
                    type=[
                        objects.inline.Standard(
                            type=objects.inline.FMTTypes.BOLD,
                            start=0,
                            end=34,
                        ),
                        objects.inline.Standard(
                            type=objects.inline.FMTTypes.ITALIC,
                            start=0,
                            end=34,
                        ),
                        objects.inline.Standard(
                            type=objects.inline.FMTTypes.SMALL,
                            start=0,
                            end=34,
                        ),
                        objects.inline.Standard(
                            type=objects.inline.FMTTypes.STRIKETHROUGH,
                            start=0,
                            end=34,
                        ),
                        objects.inline.Link(
                            type=objects.inline.FMTTypes.LINK,
                            start=0,
                            end=34,
                            url="https://en.wiktionary.org/wiki/supercalifragilisticexpialidocious",
                        )
                    ],

                    start=0,
                    end=34
                )

            ],
        ),
    ],
    tags.div(
        tags.p(
            tags.span(
                tags.b(
                    tags.i(
                        tags.small(
                            tags.s(
                                tags.a(
                                    "supercalifragilisticexpialidocious",
                                    href="https://en.wiktionary.org/wiki/supercalifragilisticexpialidocious",
                                    cls="inline-link"
                                ),
                                cls="inline-strikethrough",
                            ),
                            cls="inline-small",
                        ),
                        cls="inline-italics"
                    ),

                    cls="inline-bold",
                ),
                cls="inline-formatted-content",
            ),
            cls="text-block",
        ),
        cls="post",
    ),
)