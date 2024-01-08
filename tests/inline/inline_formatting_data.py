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
            inline_formatting=[objects.inline.StyleInterval(start=5, end=10, instructions=[objects.inline.Instruction(objects.inline.FMTTypes.SMALL)])],
        )
    ],
    tags.div(
        tags.p(
            tags.span("some ", tags.small("small", cls="inline-small"), " text", cls="inline-formatted-content"),
            cls="text-block",
        ),
        cls="post-body",
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
                objects.inline.StyleInterval(
                    start=6,
                    end=10,
                    instructions=[
                        objects.inline.LinkInstruction(
                            type_=objects.inline.FMTTypes.LINK,
                            url="https://www.nasa.gov",
                        )
                    ],
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
        cls="post-body",
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
                objects.inline.StyleInterval(
                    start=13,
                    end=19,
                    instructions=[
                        objects.inline.MentionInstruction(
                            type_=objects.inline.FMTTypes.MENTION,
                            blog_uuid="t:123456abcdf",
                            blog_name="david",
                            blog_url="https://davidslog.com/",
                        )
                    ],
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
        cls="post-body",
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
                objects.inline.StyleInterval(
                    start=10,
                    end=15,
                    instructions=[
                        objects.inline.ColorInstruction(
                            type_=objects.inline.FMTTypes.COLOR,
                            hex="#ff492f"
                        )
                    ],
                )
            ]
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
        cls="post-body",
    ),
)

