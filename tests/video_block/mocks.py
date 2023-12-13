import dominate

from npf_renderer import objects


basic_video = (
    [{
        "type": "video",
        "provider": "tumblr",
        "url": "https://va.media.tumblr.com/tumblr_some_id_720.mp4",
        "media": [{
            "url": "https://va.media.tumblr.com/tumblr_some_id_720.mp4",
            "type": "video/mp4",
            "width": 1080,
            "height": 1920
        }],

        "poster": [{
            "url": "https://64.media.tumblr.com/tumblr_some_id_frame1.jpg",
            "type": "image/jpeg",
            "width": 1080,
            "height": 1920
        }],

        "filmstrip": {
            "url": "https://64.media.tumblr.com/previews/tumblr_some_id_filmstrip.jpg",
            "type": "image/jpeg",
            "width": 2000,
            "height": 357
        }
    }],

    [
        objects.video_block.VideoBlock(
            url="https://va.media.tumblr.com/tumblr_some_id_720.mp4",
            media=[objects.media_objects.MediaObject(
                url="https://va.media.tumblr.com/tumblr_some_id_720.mp4",
                type="video/mp4",
                width=1080,
                height=1920
            )],
            provider="tumblr",
            poster=[objects.media_objects.MediaObject(
                url="https://64.media.tumblr.com/tumblr_some_id_frame1.jpg",
                type="image/jpeg",
                width=1080,
                height=1920
            )],
            filmstrip=[objects.media_objects.MediaObject(
                url="https://64.media.tumblr.com/previews/tumblr_some_id_filmstrip.jpg",
                type="image/jpeg",
                width=2000,
                height=357
            )],
        )
    ],

    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.video(
                    dominate.tags.source(src="https://va.media.tumblr.com/tumblr_some_id_720.mp4", type="video/mp4"),
                    width=1080,
                    height=1920,
                    preload="none",
                    controls=True,
                    poster="https://64.media.tumblr.com/tumblr_some_id_frame1.jpg"
                ),
                cls="video-container"
            ),
            cls="video-block"
        ),
        cls="post-body"
    )
)


simplest_possible_video = (
    [{
        "type": "video",
        "url": "https://va.media.tumblr.com/tumblr_some_id_720.mp4",
        "media": [{
            "url": "https://va.media.tumblr.com/tumblr_some_id_720.mp4",
            "type": "video/mp4",
            "width": 1080,
            "height": 1920
        }],
    }],

    [
        objects.video_block.VideoBlock(
            url="https://va.media.tumblr.com/tumblr_some_id_720.mp4",
            media=[objects.media_objects.MediaObject(
                url="https://va.media.tumblr.com/tumblr_some_id_720.mp4",
                type="video/mp4",
                width=1080,
                height=1920
            )],
        )
    ],

    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.video(
                    dominate.tags.source(src="https://va.media.tumblr.com/tumblr_some_id_720.mp4", type="video/mp4"),
                    width=1080,
                    height=1920,
                    preload="none",
                    controls=True,
                ),
                cls="video-container"
            ),
            cls="video-block"
        ),
        cls="post-body"
    )
)


embedded_arbitrary_video = (
    [{
        "type": "video",
        "provider": "example",
        "url": "https://example.com/someid",
        "embedHtml": """<iframe width="356" height="200"  id="example-iframe" src="https://example.com/embed/someid""",
        "poster": [{
            "url": "https://64.media.tumblr.com/da7eee219695668e3892e06d/6156e3a00edaed-53/s500x750/33081d7dbf6189c442ef.jpg",
            "type": "image/jpeg",
            "width": 480,
            "height": 360
        }],
        "embedIframe": {
            "url": "https://safe.txmblr.com/svc/embed/inline/https%3A%2F%2Fwww.example.com%2Fwatch%3Fv%3someid#embed-3578ffc1cd5886",
            "width": 356,
            "height": 200,
        }
    }],

    [
        objects.video_block.VideoBlock(
            url="https://example.com/someid",
            provider="example",
            poster=[objects.media_objects.MediaObject(
                url="https://64.media.tumblr.com/da7eee219695668e3892e06d/6156e3a00edaed-53/s500x750/33081d7dbf6189c442ef.jpg",
                type="image/jpeg",
                width=480,
                height=360
            )],
            embed_html="""<iframe width="356" height="200"  id="example-iframe" src="https://example.com/embed/someid""",
            embed_iframe=objects.video_block.EmbedIframeObject(
                url="https://safe.txmblr.com/svc/embed/inline/https%3A%2F%2Fwww.example.com%2Fwatch%3Fv%3someid#embed-3578ffc1cd5886",
                width=356,
                height=200
            )
        )
    ],

    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.iframe(
                    src="https://safe.txmblr.com/svc/embed/inline/https%3A%2F%2Fwww.example.com%2Fwatch%3Fv%3someid#embed-3578ffc1cd5886",
                    width=356,
                    height=200,
                    scrolling="no",
                    frameborder="0",
                    title="example"
                ),
                cls="video-container"
            ),
            cls="video-block"
        ),
        cls="post-body"
    )
)


embedded_youtube_video = (
    [{
        "type": "video",
        "provider": "youtube",
        "url": "https://www.youtube.com/watch?v=someid",
        "embedHtml": """<iframe width="356" height="200"  id="youtube_iframe" src="https://www.youtube.com/embed/someid?feature=oembed&amp;enablejsapi=1&amp;origin=https://safe.txmblr.com&amp;wmode=opaque" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen title="some title"></iframe>""",
        "poster": [{
            "url": "https://64.media.tumblr.com/da7eee219695668e3892e06d/6156e3a00edaed-53/s500x750/33081d7dbf6189c442ef.jpg",
            "type": "image/jpeg",
            "width": 480,
            "height": 360
        }],
        "embedIframe": {
            "url": "https://safe.txmblr.com/svc/embed/inline/https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3someid#embed-3578ffc1cd5886",
            "width": 356,
            "height": 200,
        }
    }],

    [
        objects.video_block.VideoBlock(
            url="https://www.youtube.com/watch?v=someid",
            provider="youtube",
            poster=[objects.media_objects.MediaObject(
                url="https://64.media.tumblr.com/da7eee219695668e3892e06d/6156e3a00edaed-53/s500x750/33081d7dbf6189c442ef.jpg",
                type="image/jpeg",
                width=480,
                height=360
            )],
            embed_html="""<iframe width="356" height="200"  id="youtube_iframe" src="https://www.youtube.com/embed/someid?feature=oembed&amp;enablejsapi=1&amp;origin=https://safe.txmblr.com&amp;wmode=opaque" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen title="some title"></iframe>""",
            embed_iframe=objects.video_block.EmbedIframeObject(
                url="https://safe.txmblr.com/svc/embed/inline/https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3someid#embed-3578ffc1cd5886",
                width=356,
                height=200
            )
        )
    ],

    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.iframe(
                    src="https://safe.txmblr.com/svc/embed/inline/https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3someid#embed-3578ffc1cd5886",
                    width=356,
                    height=300,
                    scrolling="no",
                    frameborder="0",
                    title="youtube"
                ),
                cls="video-container"
            ),
            cls="video-block"
        ),
        cls="post-body"
    )
)


embedded_forbid_external_iframes_fallback = (
    embedded_youtube_video[0],
    embedded_youtube_video[1],

    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.a(
                dominate.tags.div(
                    dominate.tags.img(
                        alt="youtube",
                        sizes="(max-width: 540px) 100vh, 540px",
                        srcset="https://64.media.tumblr.com/da7eee219695668e3892e06d/6156e3a00edaed-53/s500x750/33081d7dbf6189c442ef.jpg 480w",
                    ),

                    dominate.tags.div(
                        dominate.tags.span("Embedded videos are not supported"),
                        cls="link-block-title poster-overlay-text"
                    ),
                    cls="poster-container"
                ),

                dominate.tags.div(
                    dominate.tags.p("Please click me to visit \"youtube\" to watch the video", cls="link-block-description"),
                    dominate.tags.div(dominate.tags.span(dominate.tags.span("youtube")), cls="link-block-subtitles"),
                    cls="link-block-description-container"
                ),

                href="https://www.youtube.com/watch?v=someid",
                cls="link-block-link"
            ),
            cls="link-block"
        ),
        cls="post-body"
    )
)
