from npf_renderer import objects


simple_link_block = (
    {"content": [{"type": "link", "url": "https://example.com"}]},
    [
        objects.link_block.LinkBlock(
            url="https://example.com"
        )
    ]
)


link_block_with_title = (
    {"content": [{"type": "link", "url": "https://example.com", "title": "Example Domain"}]},
    [
        objects.link_block.LinkBlock(
            url="https://example.com",
            title="Example Domain"
        )
    ]
)


link_block_with_description = (
    {"content": [{"type": "link", "url": "https://example.com", "description": "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission."}]},
    [
        objects.link_block.LinkBlock(
            url="https://example.com",
            description="This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission."
        )
    ]
)


link_block_with_title_and_description = (
    {"content": [{"type": "link", "url": "https://example.com", "title": "Example Domain", "description": "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission."}]},
    [
        objects.link_block.LinkBlock(
            url="https://example.com",
            title="Example Domain",
            description="This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission."
        )
    ]
)


link_block_with_site_name = (
    {"content": [{"type": "link", "url": "https://example.com", "siteName": "Example Domain"}]},
    [
        objects.link_block.LinkBlock(
            url="https://example.com",
            site_name="Example Domain"
        )
    ]
)


link_block_with_site_name_and_author = (
    {"content": [{"type": "link", "url": "https://example.com", "siteName": "Example Domain", "author": "Example Author"}]},
    [
        objects.link_block.LinkBlock(
            url="https://example.com",
            site_name="Example Domain",
            author="Example Author"
        )
    ]
)


link_block_with_poster = (
    {"content": [{"type": "link", "url": "https://example.com", "poster": [{
        "mediaKey": "c5c8a00f5c269bda091df0020ca48",
        "type": "image/jpeg",
        "width": 1280,
        "height": 720,
        "url": "https://example.com/image"
    }]}]},
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
            ]
        )
    ]
)


link_block_with_all = (
    {"content": [{
        "type": "link",
        "url": "https://example.com",
        "title": "Example Domain",
        "description": "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
        "siteName": "Example Domain",
        "author": "Example Author",
        "poster": [{
            "mediaKey": "c5c8a00f5c269bda091df0020ca48",
            "type": "image/jpeg",
            "width": 1280,
            "height": 720,
            "url": "https://example.com/image"
        }]
    }]},

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
            ]

        )
    ]
)
