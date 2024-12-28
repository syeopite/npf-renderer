import dominate

from npf_renderer import objects


def format_constructor(url, *children):
    return dominate.tags.div(
        dominate.tags.div(dominate.tags.a(*children, href=url, cls="link-block-link"), cls="link-block"),
        cls="post-body",
    )


simple_link_block = (
    {"content": [{"type": "link", "url": "https://example.com"}]},
    [objects.link_block.LinkBlock(url="https://example.com")],
    format_constructor(
        "https://example.com",
        dominate.tags.div(
            dominate.tags.div(dominate.tags.span(dominate.tags.span("example.com")), cls="link-block-subtitles"),
            cls="link-block-description-container",
        ),
    ),
)


link_block_with_title = (
    {"content": [{"type": "link", "url": "https://example.com", "title": "Example Domain"}]},
    [objects.link_block.LinkBlock(url="https://example.com", title="Example Domain")],
    format_constructor(
        "https://example.com",
        dominate.tags.div(dominate.tags.span("Example Domain"), cls="link-block-title"),
        dominate.tags.div(
            dominate.tags.div(dominate.tags.span(dominate.tags.span("example.com")), cls="link-block-subtitles"),
            cls="link-block-description-container",
        ),
    ),
)


link_block_with_description = (
    {
        "content": [
            {
                "type": "link",
                "url": "https://example.com",
                "description": "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
            }
        ]
    },
    [
        objects.link_block.LinkBlock(
            url="https://example.com",
            description="This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
        )
    ],
    format_constructor(
        "https://example.com",
        dominate.tags.div(
            dominate.tags.p(
                "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
                cls="link-block-description",
            ),
            dominate.tags.div(dominate.tags.span(dominate.tags.span("example.com")), cls="link-block-subtitles"),
            cls="link-block-description-container",
        ),
    ),
)


link_block_with_title_and_description = (
    {
        "content": [
            {
                "type": "link",
                "url": "https://example.com",
                "title": "Example Domain",
                "description": "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
            }
        ]
    },
    [
        objects.link_block.LinkBlock(
            url="https://example.com",
            title="Example Domain",
            description="This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
        )
    ],
    format_constructor(
        "https://example.com",
        dominate.tags.div(dominate.tags.span("Example Domain"), cls="link-block-title"),
        dominate.tags.div(
            dominate.tags.p(
                "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
                cls="link-block-description",
            ),
            dominate.tags.div(dominate.tags.span(dominate.tags.span("example.com")), cls="link-block-subtitles"),
            cls="link-block-description-container",
        ),
    ),
)


link_block_with_site_name = (
    {"content": [{"type": "link", "url": "https://example.com", "siteName": "Example Domain"}]},
    [objects.link_block.LinkBlock(url="https://example.com", site_name="Example Domain")],
    format_constructor(
        "https://example.com",
        dominate.tags.div(
            dominate.tags.div(dominate.tags.span(dominate.tags.span("Example Domain")), cls="link-block-subtitles"),
            cls="link-block-description-container",
        ),
    ),
)


link_block_with_site_name_and_author = (
    {
        "content": [
            {"type": "link", "url": "https://example.com", "siteName": "Example Domain", "author": "Example Author"}
        ]
    },
    [objects.link_block.LinkBlock(url="https://example.com", site_name="Example Domain", author="Example Author")],
    format_constructor(
        "https://example.com",
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.span(
                    dominate.tags.span("Example Domain"),
                    dominate.tags.span("|", cls="site-name-author-separator"),
                    dominate.tags.span("Example Author"),
                ),
                cls="link-block-subtitles",
            ),
            cls="link-block-description-container",
        ),
    ),
)


link_block_with_poster = (
    {
        "content": [
            {
                "type": "link",
                "url": "https://example.com",
                "poster": [
                    {
                        "mediaKey": "c5c8a00f5c269bda091df0020ca48",
                        "type": "image/jpeg",
                        "width": 1280,
                        "height": 720,
                        "url": "https://example.com/image",
                    }
                ],
            }
        ]
    },
    [
        objects.link_block.LinkBlock(
            url="https://example.com",
            poster=[
                objects.media_objects.MediaObject(
                    url="https://example.com/image",
                    width=1280,
                    height=720,
                    type="image/jpeg",
                )
            ],
        )
    ],
    format_constructor(
        "https://example.com",
        dominate.tags.div(
            dominate.tags.img(
                alt="Preview image for \"https://example.com\"",
                sizes="(max-width: 540px) 100vh, 540px",
                srcset="https://example.com/image 1280w",
            ),
            cls="poster-container",
        ),
        dominate.tags.div(
            dominate.tags.div(dominate.tags.span(dominate.tags.span("example.com")), cls="link-block-subtitles"),
            cls="link-block-description-container",
        ),
    ),
)


link_block_with_all = (
    {
        "content": [
            {
                "type": "link",
                "url": "https://example.com",
                "title": "Example Domain",
                "description": "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
                "siteName": "Example Domain",
                "author": "Example Author",
                "poster": [
                    {
                        "mediaKey": "c5c8a00f5c269bda091df0020ca48",
                        "type": "image/jpeg",
                        "width": 1280,
                        "height": 720,
                        "url": "https://example.com/image",
                    }
                ],
            }
        ]
    },
    [
        objects.link_block.LinkBlock(
            url="https://example.com",
            title="Example Domain",
            description="This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
            site_name="Example Domain",
            author="Example Author",
            poster=[
                objects.media_objects.MediaObject(
                    url="https://example.com/image",
                    width=1280,
                    height=720,
                    type="image/jpeg",
                )
            ],
        )
    ],
    format_constructor(
        "https://example.com",
        dominate.tags.div(
            dominate.tags.img(
                alt="Example Domain",
                sizes="(max-width: 540px) 100vh, 540px",
                srcset="https://example.com/image 1280w",
            ),
            dominate.tags.div(dominate.tags.span("Example Domain"), cls="link-block-title poster-overlay-text"),
            cls="poster-container",
        ),
        dominate.tags.div(
            dominate.tags.p(
                "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
                cls="link-block-description",
            ),
            dominate.tags.div(
                dominate.tags.span(
                    dominate.tags.span("Example Domain"),
                    dominate.tags.span("|", cls="site-name-author-separator"),
                    dominate.tags.span("Example Author"),
                ),
                cls="link-block-subtitles",
            ),
            cls="link-block-description-container",
        ),
    ),
)
