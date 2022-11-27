import dominate.tags

from npf_renderer.objects import attribution


blog_attribution = (
    {
        "type": "blog",
        "url": "https://example.tumblr.com",

        "blog": {
            "name": "example",
            "avatar": [
                {"width": 512, "height": 512, "url": "https://example.com/512/example.png"},
                {"width": 256, "height": 256, "url": "https://example.com/256/example.png"},
                {"width": 128, "height": 128, "url": "https://example.com/128/example.png"}
            ],
            "uuid": "t:SN32hxaWHi312_32_df"
        }
    },

    attribution.BlogAttribution(
        url="https://example.tumblr.com",
        uuid="t:SN32hxaWHi312_32_df",
        name="example",

        avatar=[
            attribution.MediaObject(width=512, height=512, url="https://example.com/512/example.png"),
            attribution.MediaObject(width=256, height=256, url="https://example.com/256/example.png"),
            attribution.MediaObject(width=128, height=128, url="https://example.com/128/example.png"),
        ]
    ),

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

            dominate.tags.div(cls="ask-content"),

            cls="ask-body"
        ),

        dominate.tags.img(
            src="https://example.com/512/example.png",
            cls="avatar asker-avatar image", loading="lazy"
        ),

        cls="ask"
    )
)


post_attribution = (
    {
        "type": "post",
        "url": "https://example.tumblr.com/post/123456789123/example-post-slug-here",
        "post": {"id": "123456789123"},

        "blog": {
            "name": "example",
            "url": "https://example.tumblr.com",
            "uuid": "t:SN32hxaWHi312_32_df"
        }
    },

    attribution.PostAttribution(
        url="https://example.tumblr.com/post/123456789123/example-post-slug-here",
        post="123456789123",
        blog=attribution.BlogAttribution(
            name="example",
            url="https://example.tumblr.com",
            uuid="t:SN32hxaWHi312_32_df"
        )
    ),

    dominate.tags.div(
        dominate.tags.a(
            "From ",
            dominate.tags.b(
                "example"
            ),
            href="https://example.tumblr.com/post/123456789123/example-post-slug-here",
        ),
        cls="post-attribution"
    )
)


link_attribution = (
    {
        "type": "link",
        "url": "https://example.com",
    },

    attribution.LinkAttribution(
        url="https://example.com",
    ),

    dominate.tags.div(
        dominate.tags.a(
            "example.com",
            href="https://example.com",
        ),
        cls="link-attribution"
    )
)


app_attribution = (
    {
        "type": "app",
        "appName": "SoundCloud",
        "url": "https://soundcloud.com/example/example-track",
        "logo": {
            "url": "https://static.tumblr.com/f92f127280909cfd34d802e241dfef3f/iebsmgz"
                   "/lIVnsx8an/tumblr_static_soundcloud_logo.png",
            "type": "image/png",
            "width": 128,
            "height": 128
        },

        "displayText": "Listen on"
    },

    attribution.AppAttribution(
        url="https://soundcloud.com/example/example-track",
        app_name="SoundCloud",
        display_text="Listen on",

        logo=attribution.MediaObject(
            url="https://static.tumblr.com/f92f127280909cfd34d802e241dfef3f/iebsmgz"
                "/lIVnsx8an/tumblr_static_soundcloud_logo.png",
            type="image/png",
            width=128,
            height=128
        )
    )
)
