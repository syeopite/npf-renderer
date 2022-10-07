from dominate import tags


connected_back_to_back_inline_format_test = (
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
        cls="post",
    ),
)

back_to_back_inline_format_test = (
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
        cls="post",
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
        cls="post",
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
                tags.span(
                    "brown ",
                    tags.b(
                        "fox",
                        cls="inline-bold"
                    ),
                    " jumped over",
                    cls="inline-color",
                    style="color: #964B00;",
                ),
                " the lazy dog",

                cls="inline-formatted-content"
            ),

            cls="text-block indented inline-formatted-block",
        ),

        cls="post"
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
                tags.span(
                    "br",
                    tags.small(
                        "own ",
                        tags.b(
                            "fox",
                            cls="inline-bold"
                        ),
                        " ",
                        cls="inline-small",
                    ),
                    "jumped over",
                    cls="inline-color",
                    style="color: #964B00;",
                ),
                " the lazy dog",

                cls="inline-formatted-content"
            ),

            cls="text-block indented inline-formatted-block",
        ),

        cls="post"
    )
)