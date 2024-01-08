"""Additional test data for the formatter.

As the formatter is far more complex than the parser, it needs more tests.
"""

from dominate import tags

connected_back_to_back_format_test = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "indented",
            "formatting": [
                {"start": 4, "end": 10, "type": "color", "hex": "#964B00"},
                {"start": 10, "end": 13, "type": "link", "url": "https://www.youtube.com/watch?v=jofNR_WkoCE"},
                {"start": 13, "end": 20, "type": "bold"},
                {"start": 20, "end": 30, "type": "small"},
                {"start": 30, "end": 38, "type": "italic"},
            ],
        }
    ],
    tags.div(
        tags.blockquote(
            tags.span(
                "The ",
                tags.span(
                    "brown ",
                    cls="inline-color",
                    style="color: #964B00;",
                ),
                tags.a("fox", href="https://www.youtube.com/watch?v=jofNR_WkoCE", cls="inline-link"),
                tags.b(" jumped", cls="inline-bold"),
                tags.small(" over the ", cls="inline-small"),
                tags.i("lazy dog", cls="inline-italics"),
                cls="inline-formatted-content",
            ),
            cls="text-block indented inline-formatted-block",
        ),
        cls="post-body",
    ),
)


back_to_back_format_test = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "indented",
            "formatting": [
                {"start": 4, "end": 9, "type": "color", "hex": "#964B00"},
                {"start": 10, "end": 13, "type": "link", "url": "https://www.youtube.com/watch?v=jofNR_WkoCE"},
                {"start": 14, "end": 20, "type": "bold"},
                {"start": 21, "end": 29, "type": "small"},
                {"start": 30, "end": 38, "type": "italic"},
            ],
        }
    ],
    tags.div(
        tags.blockquote(
            tags.span(
                "The ",
                tags.span(
                    "brown",
                    cls="inline-color",
                    style="color: #964B00;",
                ),
                " ",
                tags.a("fox", href="https://www.youtube.com/watch?v=jofNR_WkoCE", cls="inline-link"),
                " ",
                tags.b("jumped", cls="inline-bold"),
                " ",
                tags.small("over the", cls="inline-small"),
                " ",
                tags.i("lazy dog", cls="inline-italics"),
                cls="inline-formatted-content",
            ),
            cls="text-block indented inline-formatted-block",
        ),
        cls="post-body",
    ),
)


long_space_in_between_format_test = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "indented",
            "formatting": [
                {"start": 4, "end": 10, "type": "color", "hex": "#964B00"},
                {"start": 30, "end": 38, "type": "italic"},
            ],
        }
    ],
    tags.div(
        tags.blockquote(
            tags.span(
                "The ",
                tags.span(
                    "brown ",
                    cls="inline-color",
                    style="color: #964B00;",
                ),
                "fox jumped over the ",
                tags.i("lazy dog", cls="inline-italics"),
                cls="inline-formatted-content",
            ),
            cls="text-block indented inline-formatted-block",
        ),
        cls="post-body",
    ),
)


second_has_lower_end_index_test = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "indented",
            "formatting": [
                {"start": 4, "end": 25, "type": "color", "hex": "#964B00"},
                {"start": 10, "end": 13, "type": "bold"},
            ],
        }
    ],
    tags.div(
        tags.blockquote(
            tags.span(
                "The ",
                tags.span("brown ", cls="inline-color", style="color: #964B00;"),
                tags.b(
                    tags.span(
                        "fox",
                        cls="inline-color",
                        style="color: #964B00;"
                    ),
                    cls="inline-bold",
                ),
                tags.span(" jumped over", cls="inline-color", style="color: #964B00;"),
                " the lazy dog",
                cls="inline-formatted-content"
            ),
            cls="text-block indented inline-formatted-block",
        ),

        cls="post-body"
    )
)


second_has_lower_end_index_test_2 = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "indented",
            "formatting": [
                {"start": 4, "end": 25, "type": "color", "hex": "#964B00"},
                {"start": 6, "end": 14, "type": "small"},
                {"start": 10, "end": 13, "type": "bold"},
            ],
        }
    ],
    tags.div(
        tags.blockquote(
            tags.span(
                "The ",
                tags.span("br", cls="inline-color", style="color: #964B00;"),
                tags.small(
                    tags.span(
                        "own ",
                        cls="inline-color",
                        style="color: #964B00;"
                    ),
                    cls="inline-small", 
                ),
                tags.b(
                    tags.small(
                        tags.span(
                            "fox",
                        cls="inline-color", 
                        style="color: #964B00;"
                        ),
                        cls="inline-small"
                    ),
                    cls="inline-bold"
                ),

                tags.small(
                    tags.span(
                        " ",
                        cls="inline-color",
                        style="color: #964B00;"
                    ),
                    cls="inline-small"
                ),

                tags.span("jumped over", cls="inline-color", style="color: #964B00;"),
                " the lazy dog",

                cls="inline-formatted-content"
            ),

            cls="text-block indented inline-formatted-block",
        ),

        cls="post-body"
    )
)


overlapping_same_area_test_data = (
    [
        {
            "type": "text",
            "text": "The hypersonic brown fox jumped over the sleeping dog",
            "subtype": "indented",
            "formatting": [
                {"start": 4, "end": 24, "type": "color", "hex": "#964B00"},
                {"start": 4, "end": 24, "type": "link", "url": "https://www.youtube.com/watch?v=jofNR_WkoCE"},
                {"start": 4, "end": 24, "type": "bold"},
                {"start": 4, "end": 24, "type": "strikethrough"},
                {"start": 4, "end": 24, "type": "italic"},
                {"start": 4, "end": 24, "type": "small"},
            ],
        }
    ],

    tags.div(
        tags.blockquote(
            tags.span(
                "The ",
                tags.b(
                    tags.i(
                        tags.s(
                            tags.small(
                                tags.a(
                                    tags.span(
                                        "hypersonic brown fox",
                                        cls="inline-color",
                                        style="color: #964B00;"
                                    ),
                                    href="https://www.youtube.com/watch?v=jofNR_WkoCE",
                                    cls="inline-link",
                                ),
                                cls="inline-small"
                            ),
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),
                " jumped over the sleeping dog",
                cls="inline-formatted-content"
            ),
            cls="text-block indented inline-formatted-block"
        ),
        cls="post-body"
    )
)


overlapping_same_start_different_end_data = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "indented",
            "formatting": [
                {"start": 4, "end": 10, "type": "color", "hex": "#964B00"},
                {"start": 4, "end": 20, "type": "link", "url": "https://www.youtube.com/watch?v=jofNR_WkoCE"},
                {"start": 4, "end": 30, "type": "bold"},
            ],
        }
    ],

    tags.div(
        tags.blockquote(
            tags.span(
                "The ",
                tags.b(
                    tags.a(
                        tags.span(
                            "brown ",
                            style="color: #964B00;",
                            cls="inline-color"
                        ),
                        href="https://www.youtube.com/watch?v=jofNR_WkoCE",
                        cls="inline-link"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.a(
                        "fox jumped",
                        href="https://www.youtube.com/watch?v=jofNR_WkoCE",
                        cls="inline-link"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    " over the ",
                    cls="inline-bold"
                ),

                "lazy dog",

                cls="inline-formatted-content"
            ),
            cls="text-block indented inline-formatted-block"
        ),
        cls="post-body"
    )
)


interrupted_same_indices_overlapping = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "indented",
            "formatting": [
                {"start": 4, "end": 25, "type": "color", "hex": "#964B00"},
                {"start": 4, "end": 25, "type": "italic"},
                {"start": 4, "end": 25, "type": "small"},
                {"start": 2, "end": 8, "type": "link", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},

            ],
        }
    ],
    tags.div(
        tags.blockquote(
            tags.span(
                "Th",
                tags.a("e ", cls="inline-link", href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                tags.i(
                    tags.small(
                        tags.a(
                            tags.span(
                                "brow",
                                style="color: #964B00;",
                                cls="inline-color"
                            ),
                            cls="inline-link",
                            href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                        ),
                        cls="inline-small"
                    ),
                    cls="inline-italics"
                ),

                tags.i(
                    tags.small(
                        tags.span(
                            "n fox jumped over",
                            style="color: #964B00;",
                            cls="inline-color"
                        ),
                        cls="inline-small"
                    ),
                    cls="inline-italics"
                ),
                " the lazy dog",
                cls="inline-formatted-content"
            ),
            cls="text-block indented inline-formatted-block"
        ),
        cls="post-body"
    )
)


interrupted_overlap_test = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "heading1",
            "formatting": [
                {"start": 10, "end": 29, "type": "color", "hex": "#964B00"},

                {"start": 5, "end": 13, "type": "small"},
                {"start": 8, "end": 18, "type": "strikethrough"},
            ],
        }
    ],
    tags.div(
        tags.h1(
            tags.span(
                "The b",
                tags.small("row", cls="inline-small"),
                tags.s(tags.small("n ", cls="inline-small"), cls="inline-strikethrough"),
                tags.s(
                    tags.small(
                        tags.span(
                            "fox",
                            style="color: #964B00;",
                            cls="inline-color",
                        ),
                        cls="inline-small"
                    ),
                    cls="inline-strikethrough"
                ),

                tags.s(
                    tags.span(
                        " jump",
                        style="color: #964B00;",
                        cls="inline-color",
                    ),
                    cls="inline-strikethrough"
                ),

                tags.span(
                    "ed over the",
                    style="color: #964B00;",
                    cls="inline-color",
                ),

                " lazy dog",

                cls="inline-formatted-content"
            ),
            cls="text-block heading1 inline-formatted-block"
        ),
        cls="post-body"
    )
)


interrupted_overlap_test_2 = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "heading1",
            "formatting": [
                {"start": 0, "end": 33, "type": "color", "hex": "#964B00"},
                {"start": 0, "end": 30, "type": "bold"},
                {"start": 10, "end": 25, "type": "italic"},

                {"start": 5, "end": 13, "type": "small"},
                {"start": 8, "end": 20, "type": "strikethrough"},
            ],
        }
    ], tags.div(
        tags.h1(
            tags.span(
                tags.b(tags.span("The b", style="color: #964B00;", cls="inline-color"), cls="inline-bold"),
                tags.b(
                    tags.small(
                        tags.span(
                            "row", 
                            style="color: #964B00;",
                            cls="inline-color"  
                        ),
                        cls="inline-small",
                    ),
                    cls="inline-bold"
                ),
                tags.b(
                    tags.s(
                        tags.small(
                            tags.span(
                                "n ", 
                                style="color: #964B00;",
                                cls="inline-color"  
                            ),
                            cls="inline-small",
                        ),
                        cls="inline-strikethrough"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        tags.s(
                            tags.small(
                                tags.span(
                                    "fox", 
                                    style="color: #964B00;",
                                    cls="inline-color"  
                                ),
                                cls="inline-small",
                            ),
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        tags.s(
                            tags.span(
                                " jumped", 
                                style="color: #964B00;",
                                cls="inline-color"  
                            ),
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        tags.span(
                            " over", 
                            style="color: #964B00;",
                            cls="inline-color"  
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.span(
                        " the ", 
                        style="color: #964B00;",
                        cls="inline-color"  
                    ),
                    cls="inline-bold"
                ),

                tags.span(
                    "laz", 
                    style="color: #964B00;",
                    cls="inline-color"  
                ),

                "y dog",

                cls="inline-formatted-content"
            ),
            cls="text-block heading1 inline-formatted-block"
        ),
        cls="post-body"
    )
)


interrupted_overlap_test_3 = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "heading1",
            "formatting": [
                {"start": 10, "end": 25, "type": "italic"},  # 'fox jumped over'

                {"start": 5, "end": 13, "type": "small"},  # 'rown fox'
                {"start": 8, "end": 20, "type": "strikethrough"},  # 'n fox jumped'
                {"start": 12, "end": 28, "type": "bold"},  # 'x jumped over th'
                {"start": 14, "end": 33, "type": "color", "hex": "#964B00"},  # 'jumped over the laz'

            ],
        }
    ], tags.div(
        tags.h1(
            tags.span(
                "The b",
                tags.small("row", cls="inline-small"),
                tags.s(tags.small("n ", cls="inline-small"), cls="inline-strikethrough"),
                tags.i(tags.s(tags.small("fo", cls="inline-small"), cls="inline-strikethrough"), cls="inline-italics"),
                tags.b(tags.i(tags.s(tags.small("x", cls="inline-small"), cls="inline-strikethrough"), cls="inline-italics"), cls="inline-bold"),
                tags.b(
                    tags.i(
                        tags.s(
                            " ",
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        tags.s(
                            tags.span(
                                "jumped",
                                style="color: #964B00;",
                                cls="inline-color"
                            ),
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        tags.span(
                            " over",
                            style="color: #964B00;",
                            cls="inline-color"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.span(
                        " th",
                        style="color: #964B00;",
                        cls="inline-color"
                    ),
                    cls="inline-bold"
                ),

                tags.span("e laz", style="color: #964B00;", cls="inline-color"),
                "y dog",
                cls="inline-formatted-content"
            ),
            cls="text-block heading1 inline-formatted-block"
        ),
        cls="post-body"
    )
)


interrupted_overlap_test_4 = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "heading1",
            "formatting": [
                {"start": 10, "end": 25, "type": "italic"},  # 'fox jumped over'
                {"start": 5, "end": 13, "type": "small"},  # 'rown fox'
                {"start": 8, "end": 20, "type": "strikethrough"},  # 'n fox jumped'
                {"start": 12, "end": 28, "type": "bold"},  # 'x jumped over th'
                {"start": 14, "end": 36, "type": "color", "hex": "#964B00"},  # 'jumped over the lazy d'
                {"start": 35, "end": 38, "type": "color", "hex": "#FFFFFF"},  # 'dog'

            ],
        }
    ], tags.div(
        tags.h1(
            tags.span(
                "The b",
                tags.small("row", cls="inline-small"),
                tags.s(tags.small("n ", cls="inline-small"), cls="inline-strikethrough"),
                tags.i(tags.s(tags.small("fo", cls="inline-small"),cls="inline-strikethrough"), cls="inline-italics"),
                tags.b(
                    tags.i(
                        tags.s(
                            tags.small("x", cls="inline-small"),
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),
                tags.b(
                    tags.i(
                        tags.s(
                            " ",
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),
                tags.b(
                    tags.i(
                        tags.s(
                            tags.span(
                                "jumped",
                                style="color: #964B00;",
                                cls="inline-color"
                            ),
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        tags.span(
                            " over",
                            style="color: #964B00;",
                            cls="inline-color"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.span(
                        " th",
                        style="color: #964B00;",
                        cls="inline-color"
                    ),
                    cls="inline-bold"
                ),

                tags.span(
                    "e lazy ",
                    style="color: #964B00;",
                    cls="inline-color"
                ),

                tags.span(
                    tags.span(
                        "d",
                        style="color: #FFFFFF;",
                        cls="inline-color"
                    ),
                    style="color: #964B00;",
                    cls="inline-color"
                ),

                tags.span(
                    "og",
                    style="color: #FFFFFF;",
                    cls="inline-color"
                ),

                cls="inline-formatted-content"
            ),
            cls="text-block heading1 inline-formatted-block"
        ),
        cls="post-body"
    )
)


interrupted_overlap_test_5 = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "heading1",
            "formatting": [
                {"start": 10, "end": 25, "type": "italic"},  # 'fox jumped over'
                {"start": 5, "end": 13, "type": "small"},  # 'rown fox'
                {"start": 8, "end": 20, "type": "strikethrough"},  # 'n fox jumped'
                {"start": 12, "end": 22, "type": "bold"},  # 'x jumped o'

            ],
        }
    ], tags.div(
        tags.h1(
            tags.span(
                "The b",
                tags.small("row", cls="inline-small"),
                tags.s(
                    tags.small("n ", cls="inline-small"),
                    cls="inline-strikethrough"
                ),
                tags.i(
                    tags.s(
                        tags.small("fo", cls="inline-small"),
                        cls="inline-strikethrough"
                    ),
                    cls="inline-italics"
                ),
                tags.b(
                    tags.i(
                        tags.s(
                            tags.small("x", cls="inline-small"),
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        tags.s(
                            " jumped",
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        " o",
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.i(
                    "ver",
                    cls="inline-italics"
                ),

                " the lazy dog",

                cls="inline-formatted-content"
            ),
            cls="text-block heading1 inline-formatted-block"
        ),
        cls="post-body"
    )
)


interrupted_overlap_test_6 = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "heading1",
            "formatting": [
                {"start": 10, "end": 25, "type": "italic"},  # 'fox jumped over'
                {"start": 10, "end": 25, "type": "link", "url": "example.com"},
                {"start": 10, "end": 25, "type": "color", "hex": "#FFFFFF"},

                {"start": 5, "end": 13, "type": "small"},  # 'rown fox'
                {"start": 8, "end": 20, "type": "strikethrough"},  # 'n fox jumped'
                {"start": 12, "end": 22, "type": "bold"},  # 'x jumped o'

            ],
        }
    ], tags.div(
        tags.h1(
            tags.span(
                "The b",
                tags.small("row", cls="inline-small"),
                tags.s(tags.small("n ", cls="inline-small"), cls="inline-strikethrough"),
                tags.i(
                    tags.s(
                        tags.small(
                            tags.a(
                                tags.span(
                                    "fo",
                                    style="color: #FFFFFF;",
                                    cls="inline-color"
                                ),
                                href="example.com",
                                cls="inline-link"
                            ),
                            cls="inline-small"
                        ),
                        cls="inline-strikethrough"
                    ),
                    cls="inline-italics"
                ),
                tags.b(
                    tags.i(
                        tags.s(
                            tags.small(
                                tags.a(
                                    tags.span(
                                        "x",
                                        style="color: #FFFFFF;",
                                        cls="inline-color"
                                    ),
                                    href="example.com",
                                    cls="inline-link"
                                ),
                                cls="inline-small"
                            ),
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        tags.s(
                            tags.a(
                                tags.span(
                                    " jumped",
                                    style="color: #FFFFFF;",
                                    cls="inline-color"
                                ),
                                href="example.com",
                                cls="inline-link"
                            ),
                            cls="inline-strikethrough"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.b(
                    tags.i(
                        tags.a(
                            tags.span(
                                " o",
                                style="color: #FFFFFF;",
                                cls="inline-color"
                            ),
                            href="example.com",
                            cls="inline-link"
                        ),
                        cls="inline-italics"
                    ),
                    cls="inline-bold"
                ),

                tags.i(
                    tags.a(
                        tags.span(
                            "ver",
                            style="color: #FFFFFF;",
                            cls="inline-color"
                        ),
                        href="example.com",
                        cls="inline-link"
                    ),
                    cls="inline-italics"
                ),

                " the lazy dog",
                cls="inline-formatted-content"
            ),
            cls="text-block heading1 inline-formatted-block"
        ),
        cls="post-body"
    )
)


same_index_with_other_overlap_test = (
    [
        {
            "type": "text",
            "text": "The brown fox jumped over the lazy dog",
            "subtype": "heading1",
            "formatting": [
                {"start": 10, "end": 20, "type": "color", "hex": "#964B00"},
                {"start": 15, "end": 30, "type": "italic"},

                {"start": 0, "end": 9, "type": "color", "hex": "#FFFFFF"},
                {"start": 0, "end": 9, "type": "bold"},

            ],
        }
    ],
    tags.div(
        tags.h1(
            tags.span(
                tags.b(
                    tags.span(
                        "The brown",
                        style="color: #FFFFFF;",
                        cls="inline-color"
                    ),
                    cls="inline-bold",
                ),
                " ",
                tags.span(
                    "fox j",
                    style="color: #964B00;",
                    cls="inline-color",
                ),

                tags.i(
                    tags.span(
                        "umped",
                        style="color: #964B00;",
                        cls="inline-color"
                    ),
                    cls="inline-italics",
                ),

                tags.i(
                    " over the ",
                    cls="inline-italics"
                ),

                "lazy dog",

                cls="inline-formatted-content"
            ),
            cls="text-block heading1 inline-formatted-block"
        ),
        cls="post-body"
    )
)


link_url_handler_test_data = (
    [
        {
            "type": "text",
            "subtype": "heading1",
            "text": "A bunch of links",
        },

        {
            "type": "text",
            "subtype": "unordered-list-item",
            "indent_level": 0,
            "text": "Twitter",
            "formatting": [
                {"start": 0, "end": 7, "type": "link", "url": "https://www.twitter.com/"}
            ],
        },

        {
            "type": "text",
            "subtype": "unordered-list-item",
            "indent_level": 0,
            "text": "YouTube",
            "formatting": [
                {"start": 0, "end": 7, "type": "link", "url": "https://www.youtube.com/"}
            ],
        },

        {
            "type": "text",
            "subtype": "unordered-list-item",
            "indent_level": 0,
            "text": "Reddit",
            "formatting": [
                {"start": 0, "end": 6, "type": "link", "url": "https://www.reddit.com/"}
            ],
        },
    ],

    tags.div(
        tags.h1(
            "A bunch of links",
            cls="text-block heading1"
        ),

        tags.ul(
            tags.li(
                tags.span(
                    tags.a(
                        "Twitter",
                        href="https://www.twitter.com/",
                        cls="inline-link",
                    ),
                    cls="inline-formatted-content"
                ),
                cls="text-block unordered-list-item inline-formatted-block"
            ),

            tags.li(
                tags.span(
                    tags.a(
                        "YouTube",
                        href="https://www.youtube.com/",
                        cls="inline-link",
                    ),
                    cls="inline-formatted-content"
                ),
                cls="text-block unordered-list-item inline-formatted-block"
            ),

            tags.li(
                tags.span(
                    tags.a(
                        "Reddit",
                        href="https://www.reddit.com/",
                        cls="inline-link",
                    ),
                    cls="inline-formatted-content"
                ),
                cls="text-block unordered-list-item inline-formatted-block"
            ),

            cls="unordered-list"
        ),
        cls="post-body"
    ),

    # Replaced URL
    tags.div(
        tags.h1(
            "A bunch of links",
            cls="text-block heading1"
        ),

        tags.ul(
            tags.li(
                tags.span(
                    tags.a(
                        "Twitter",
                        href="https://nitter.net/",
                        cls="inline-link",
                    ),
                    cls="inline-formatted-content"
                ),
                cls="text-block unordered-list-item inline-formatted-block"
            ),

            tags.li(
                tags.span(
                    tags.a(
                        "YouTube",
                        href="https://redirect.invidious.io/",
                        cls="inline-link",
                    ),
                    cls="inline-formatted-content"
                ),
                cls="text-block unordered-list-item inline-formatted-block"
            ),

            tags.li(
                tags.span(
                    tags.a(
                        "Reddit",
                        href="https://libredd.it/",
                        cls="inline-link",
                    ),
                    cls="inline-formatted-content"
                ),
                cls="text-block unordered-list-item inline-formatted-block"
            ),

            cls="unordered-list"
        ),
        cls="post-body"
    )
)


excessively_out_of_bounds_end_single_op_test = (
    [{
        "type": "text",
        "text": "some text",
        "subtype": "indented",

        "formatting": [{
            "type": "italic",
            "start": 0,
            "end": 57117
        }]
    }],

    tags.div(
        tags.blockquote(
            tags.span(
                tags.i("some text", cls="inline-italics"),
                cls="inline-formatted-content"
            ),
            cls="text-block indented inline-formatted-block"
        ),
        cls="post-body"
    )
)


excessively_out_of_bounds_end_multiple_op_test = (
    [{
        "type": "text",
        "text": "some text",
        "subtype": "indented",

        "formatting": [
            {
                "type": "italic",
                "start": 0,
                "end": 57117
            },

            {
                "type": "bold",
                "start": 0,
                "end": 27571
            },

        ]
    }],

    tags.div(
        tags.blockquote(
            tags.span(
                tags.b(tags.i("some text", cls="inline-italics"), cls="inline-bold"),
                cls="inline-formatted-content"
            ),
            cls="text-block indented inline-formatted-block"
        ),
        cls="post-body"
    )
)


excessively_out_of_bounds_end_overlap_test = (
    [{
        "type": "text",
        "text": "some text",
        "subtype": "indented",

        "formatting": [
            {
                "type": "italic",
                "start": 0,
                "end": 57117
            },

            {
                "type": "bold",
                "start": 0,
                "end": 57117
            },

        ]
    }],

    tags.div(
        tags.blockquote(
            tags.span(
                tags.b(tags.i("some text", cls="inline-italics"), cls="inline-bold"),
                cls="inline-formatted-content"
            ),
            cls="text-block indented inline-formatted-block"
        ),
        cls="post-body"
    )
)


excessively_out_of_bounds_end_multiple_op_differing_start_test = (
    [{
        "type": "text",
        "text": "some text",
        "subtype": "indented",

        "formatting": [
            {
                "type": "italic",
                "start": 0,
                "end": 57117
            },

            {
                "type": "bold",
                "start": 5,
                "end": 27571
            },

        ]
    }],

    tags.div(
        tags.blockquote(
            tags.span(
                tags.i("some ", cls="inline-italics"),
                tags.b(tags.i("text", cls="inline-italics"),cls="inline-bold"),
                cls="inline-formatted-content"
            ),
            cls="text-block indented inline-formatted-block"
        ),
        cls="post-body"
    )
)