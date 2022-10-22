from dominate import tags

from npf_renderer import objects

simple_test = (  # Basic Example
    {"content": [{"type": "text", "text": "Hello world!"}]},
    [
        objects.text_block.TextBlock(
            text="Hello world!",
        )
    ],
    tags.div(tags.p("Hello world!", cls="text-block"), cls="post"),
)

longer_and_with_empty_string_test = (  # Empty Space Test
    {
        "content": [
            {"type": "text", "text": "ello!"},
            {"type": "text", "text": ""},
            {"type": "text", "text": "my name is cyle!"},
        ]
    },
    [
        objects.text_block.TextBlock(text="ello!"),
        objects.text_block.TextBlock(text=""),
        objects.text_block.TextBlock(text="my name is cyle!"),
    ],
    tags.div(
        tags.p("ello!", cls="text-block"),
        tags.p("", cls="text-block"),
        tags.p("my name is cyle!", cls="text-block"),
        cls="post",
    ),
)

subtype_string_test = (
    {
        "content": [
            {"type": "text", "subtype": "heading1", "text": "New Post Forms Manifesto"},
            {
                "type": "text",
                "text": "There comes a moment in every company's life that they must redefine the rules...",
            },
            {
                "type": "text",
                "text": "We can choose to embrace this moment courageously, or we may choose to cower in fear.",
            },
        ]
    },
    [
        objects.text_block.TextBlock(
            text="New Post Forms Manifesto",
            subtype=objects.text_block.Subtypes.HEADING1,
        ),
        objects.text_block.TextBlock(
            text="There comes a moment in every company's life that they must redefine the rules..."
        ),
        objects.text_block.TextBlock(
            text="We can choose to embrace this moment courageously, or we may choose to cower in fear."
        ),
    ],
    tags.div(
        tags.h1("New Post Forms Manifesto", cls="text-block heading1"),
        tags.p(
            "There comes a moment in every company's life that they must redefine the rules...",
            cls="text-block",
        ),
        tags.p(
            "We can choose to embrace this moment courageously, or we may choose to cower in fear.",
            cls="text-block",
        ),
        cls="post",
    ),
)

subtype_string_test_2 = (
    {
        "content": [
            {"type": "text", "subtype": "heading1", "text": "Sward's Shopping List"},
            {"type": "text", "subtype": "ordered-list-item", "text": "Sword"},
            {"type": "text", "subtype": "ordered-list-item", "text": "Candy"},
            {"type": "text", "text": "But especially don't forget:"},
            {
                "type": "text",
                "subtype": "unordered-list-item",
                "text": "Death, which is uncountable on this list.",
            },
        ]
    },
    [
        objects.text_block.TextBlock(text="Sward's Shopping List", subtype=objects.text_block.Subtypes.HEADING1),
        objects.text_block.TextBlock(text="Sword", subtype=objects.text_block.Subtypes.ORDERED_LIST_ITEM),
        objects.text_block.TextBlock(text="Candy", subtype=objects.text_block.Subtypes.ORDERED_LIST_ITEM),
        objects.text_block.TextBlock(text="But especially don't forget:"),
        objects.text_block.TextBlock(
            text="Death, which is uncountable on this list.",
            subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
        ),
    ],
    tags.div(
        tags.h1("Sward's Shopping List", cls="text-block heading1"),
        tags.ol(
            tags.li("Sword", cls="text-block ordered-list-item"),
            tags.li("Candy", cls="text-block ordered-list-item"),
            cls="ordered-list",
        ),
        tags.p("But especially don't forget:", cls="text-block"),
        tags.ul(
            tags.li("Death, which is uncountable on this list.", cls="text-block unordered-list-item"),
            cls="unordered-list",
        ),
        cls="post",
    ),
)

subtype_and_indent_level_test = (
    {
        "content": [
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
        ]
    },
    [
        objects.text_block.TextBlock(text="Sward's Shopping List", subtype=objects.text_block.Subtypes.HEADING1),
        objects.text_block.TextBlock(
            text="First level: Fruit",
            subtype=objects.text_block.Subtypes.ORDERED_LIST_ITEM,
            nest=[
                objects.text_block.TextBlock(
                    text="Second level: Apples",
                    subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
                    nest=[
                        objects.text_block.TextBlock(
                            text="Third Level: Green",
                            subtype=objects.text_block.Subtypes.ORDERED_LIST_ITEM,
                        ),
                    ],
                ),
                objects.text_block.TextBlock(
                    text="Second level: Pears",
                    subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
                ),
            ],
        ),
        objects.text_block.TextBlock(
            text="First level: Pears",
            subtype=objects.text_block.Subtypes.ORDERED_LIST_ITEM,
        ),
    ],
    tags.div(
        tags.h1("Sward's Shopping List", cls="text-block heading1"),
        tags.ol(
            tags.li(
                "First level: Fruit",
                tags.ul(
                    tags.li(
                        "Second level: Apples",
                        tags.ol(
                            tags.li("Third Level: Green", cls="text-block ordered-list-item"),
                            cls="ordered-list",
                        ),
                        cls="text-block unordered-list-item",
                    ),
                    tags.li("Second level: Pears", cls="text-block unordered-list-item"),
                    cls="unordered-list",
                ),
                cls="text-block ordered-list-item",
            ),
            tags.li("First level: Pears", cls="text-block ordered-list-item"),
            cls="ordered-list",
        ),
        cls="post",
    ),
)

inline_formatting_test = (
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

inline_formatting_link_test = (
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
inline_formatting_mention_test = (
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

inline_formatting_color_test = (
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

test_inline_overlapping = (
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

test_inline_total_overlapping = (
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

top_level_list_with_children_merging_test_data = (
    {
        "content": [
            {
                "type": "text",
                "text": "I've got a bunch of links for you!",
                "subtype": "heading1",
                "formatting": [
                    {"start": 0, "end": 34, "type": "bold"}
                ],
            },

            {
                "type": "text",
                "subtype": "heading2",
                "text": "Interesting stuff",
            },

            {
                "type": "text",
                "subtype": "unordered-list-item",
                "text": "Space",
            },

            {
                "type": "text",
                "subtype": "unordered-list-item",
                "indent_level": 1,
                "text": "NASA",
                "formatting": [
                    {"start": 0, "end": 4, "type": "link", "url": "https://www.nasa.gov"}
                ],
            },

            {
                "type": "text",
                "subtype": "unordered-list-item",
                "indent_level": 1,
                "text": "ESA",
                "formatting": [
                    {"start": 0, "end": 3, "type": "link", "url": "https://www.esa.int/"}
                ],
            },

            {
                "type": "text",
                "subtype": "unordered-list-item",
                "indent_level": 1,
                "text": "SpaceX",
                "formatting": [
                    {"start": 0, "end": 6, "type": "link", "url": "https://www.spacex.com/"}
                ],
            },

            {
                "type": "text",
                "subtype": "unordered-list-item",
                "text": "Code",
            },

            {
                "type": "text",
                "subtype": "unordered-list-item",
                "indent_level": 1,
                "text": "Github",
                "formatting": [
                    {"start": 0, "end": 6, "type": "link", "url": "https://www.github.com/"}
                ],
            },

            {
                "type": "text",
                "subtype": "unordered-list-item",
                "indent_level": 1,
                "text": "Gitlab",
                "formatting": [
                    {"start": 0, "end": 6, "type": "link", "url": "https://about.gitlab.com/"}
                ],
            },
        ]
    },
    [
        objects.text_block.TextBlock(
            text="I've got a bunch of links for you!",
            subtype=objects.text_block.Subtypes.HEADING1,
            inline_formatting=[
                objects.inline.Standard(start=0, end=34, type=objects.inline.FMTTypes.BOLD)
            ]
        ),
        objects.text_block.TextBlock(text="Interesting stuff",
                                     subtype=objects.text_block.Subtypes.HEADING2),

        objects.text_block.TextBlock(
            text="Space",
            subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
            nest=[
                objects.text_block.TextBlock(
                    text="NASA",
                    inline_formatting=[
                        objects.inline.Link(
                            start=0,
                            end=4,
                            type=objects.inline.FMTTypes.LINK,
                            url="https://www.nasa.gov",
                        ),
                    ],
                    subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
                ),
                objects.text_block.TextBlock(
                    text="ESA",
                    inline_formatting=[
                        objects.inline.Link(
                            start=0,
                            end=3,
                            type=objects.inline.FMTTypes.LINK,
                            url="https://www.esa.int/",
                        ),
                    ],
                    subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
                ),
                objects.text_block.TextBlock(
                    text="SpaceX",
                    inline_formatting=[
                        objects.inline.Link(
                            start=0,
                            end=6,
                            type=objects.inline.FMTTypes.LINK,
                            url="https://www.spacex.com/",
                        ),
                    ],
                    subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
                ),
            ],
        ),
        objects.text_block.TextBlock(
            text="Code",
            subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
            nest=[
                objects.text_block.TextBlock(
                    text="Github",
                    inline_formatting=[
                        objects.inline.Link(
                            start=0,
                            end=6,
                            type=objects.inline.FMTTypes.LINK,
                            url="https://www.github.com/",
                        ),
                    ],
                    subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
                ),
                objects.text_block.TextBlock(
                    text="Gitlab",
                    inline_formatting=[
                        objects.inline.Link(
                            start=0,
                            end=6,
                            type=objects.inline.FMTTypes.LINK,
                            url="https://about.gitlab.com/",
                        ),
                    ],
                    subtype=objects.text_block.Subtypes.UNORDERED_LIST_ITEM,
                ),
            ],
        ),
    ],
    tags.div(
        tags.h1(
            tags.span(
                tags.b(
                    "I've got a bunch of links for you!",
                    cls="inline-bold"
                ),
                cls="inline-formatted-content"
            ),
            cls="text-block heading1 inline-formatted-block"
        ),

        tags.h2(
            "Interesting stuff",
            cls="text-block heading2"
        ),

        tags.ul(
            tags.li(
                "Space",
                tags.ul(
                    tags.li(
                        tags.span(
                            tags.a(
                                "NASA",
                                href="https://www.nasa.gov",
                                cls="inline-link",
                            ),
                            cls="inline-formatted-content"
                        ),
                        cls="text-block unordered-list-item inline-formatted-block"
                    ),

                    tags.li(
                        tags.span(
                            tags.a(
                                "ESA",
                                href="https://www.esa.int/",
                                cls="inline-link",
                            ),
                            cls="inline-formatted-content"
                        ),
                        cls="text-block unordered-list-item inline-formatted-block"
                    ),

                    tags.li(
                        tags.span(
                            tags.a(
                                "SpaceX",
                                href="https://www.spacex.com/",
                                cls="inline-link",
                            ),
                            cls="inline-formatted-content"
                        ),
                        cls="text-block unordered-list-item inline-formatted-block"
                    ),

                    cls="unordered-list"
                ),
                cls="text-block unordered-list-item"
            ),

            tags.li(
                "Code",
                tags.ul(
                    tags.li(
                        tags.span(
                            tags.a(
                                "Github",
                                href="https://www.github.com/",
                                cls="inline-link",
                            ),
                            cls="inline-formatted-content"
                        ),
                        cls="text-block unordered-list-item inline-formatted-block"
                    ),

                    tags.li(
                        tags.span(
                            tags.a(
                                "Gitlab",
                                href="https://about.gitlab.com/",
                                cls="inline-link",
                            ),
                            cls="inline-formatted-content"
                        ),
                        cls="text-block unordered-list-item inline-formatted-block"
                    ),
                    cls="unordered-list"
                ),
                cls="text-block unordered-list-item"
            ),

            cls="unordered-list"
        ),
        cls="post"
    ),

)
