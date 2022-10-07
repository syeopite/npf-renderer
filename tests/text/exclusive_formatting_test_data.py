from dominate import tags


back_to_back_inline_format_test = (
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
                {"start": 30, "end": 38, "type": "italic"}
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
                tags.a(
                    "fox",
                    href="https://www.youtube.com/watch?v=jofNR_WkoCE",
                    cls="inline-link"
                ),

                tags.b(
                    " jumped",
                    cls="inline-bold"
                ),

                tags.small(
                    " over the ",
                    cls="inline-small"
                ),

                tags.i(
                    "lazy dog",
                    cls="inline-italics"
                ),

                cls="inline-formatted-content"
            ),
            cls="text-block indented inline-formatted-block"
        ),
        cls="post"
    ),
)
