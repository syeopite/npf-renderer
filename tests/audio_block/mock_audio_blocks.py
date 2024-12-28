import dominate

from npf_renderer import objects


MEDIA = {
    "raw": {
        "type": "audio/mpeg",
        "url": "https://a.tumblr.com/someaudiosource.mp3",
    },
    "parsed": [
        objects.media_objects.MediaObject(
            url="https://a.tumblr.com/someaudiosource.mp3", width=540, height=405, type="audio/mpeg"
        )
    ],
    "formatted": dominate.tags.source(src="https://a.tumblr.com/someaudiosource.mp3", type="audio/mpeg"),
}

basic_audio_block = (
    {"type": "audio", "provider": "tumblr", "url": "https://a.tumblr.com/someaudiosource.mp3", "media": MEDIA["raw"]},
    [
        objects.audio_block.AudioBlock(
            url="https://a.tumblr.com/someaudiosource.mp3", provider="tumblr", media=MEDIA["parsed"]
        )
    ],
    dominate.tags.section(dominate.tags.audio(MEDIA["formatted"], controls=True), cls="ap-container"),
)


audio_block_with_title = (
    {**basic_audio_block[0], "title": "Example title"},
    [
        objects.audio_block.AudioBlock(
            url="https://a.tumblr.com/someaudiosource.mp3",
            provider="tumblr",
            title="Example title",
            media=MEDIA["parsed"],
        )
    ],
    dominate.tags.section(
        dominate.tags.header(
            dominate.tags.div(dominate.tags.h3("Example title", cls="ab-title"), cls="ab-metadata"), cls="ab-heading"
        ),
        dominate.tags.audio(MEDIA["formatted"], controls=True),
        cls="ap-container",
    ),
)


audio_block_with_metadata = (
    {**audio_block_with_title[0], "artist": "Example artist", "album": "Example album"},
    [
        objects.audio_block.AudioBlock(
            url="https://a.tumblr.com/someaudiosource.mp3",
            provider="tumblr",
            title="Example title",
            artist="Example artist",
            album="Example album",
            media=MEDIA["parsed"],
        )
    ],
    dominate.tags.section(
        dominate.tags.header(
            dominate.tags.div(
                dominate.tags.h3("Example title", cls="ab-title"),
                dominate.tags.h4("Example artist", cls="ab-artist"),
                dominate.tags.h4("Example album", cls="ab-album"),
                cls="ab-metadata",
            ),
            cls="ab-heading",
        ),
        dominate.tags.audio(MEDIA["formatted"], controls=True),
        cls="ap-container",
    ),
)


audio_block_with_poster = (
    {
        **basic_audio_block[0],
        "poster": {
            "type": "image/png",
            "url": "https://media.tumblr.com/someimage.png",
        },
    },
    [
        objects.audio_block.AudioBlock(
            url="https://a.tumblr.com/someaudiosource.mp3",
            provider="tumblr",
            media=MEDIA["parsed"],
            poster=[
                objects.media_objects.MediaObject(
                    url="https://media.tumblr.com/someimage.png", width=540, height=405, type="image/png"
                )
            ],
        )
    ],
    dominate.tags.section(
        dominate.tags.header(
            dominate.tags.img(
                src="https://media.tumblr.com/someimage.png",
                srcset="https://media.tumblr.com/someimage.png 540w",
                sizes="(max-width: 540px) 100vh, 540px",
                alt="Album art",
                cls="ab-poster",
            ),
            cls="ab-heading",
        ),
        dominate.tags.audio(MEDIA["formatted"], controls=True),
        cls="ap-container",
    ),
)


audio_block_with_metadata_and_poster = (
    {
        **audio_block_with_metadata[0],
        "poster": audio_block_with_poster[0]["poster"],
    },
    [
        objects.audio_block.AudioBlock(
            url="https://a.tumblr.com/someaudiosource.mp3",
            provider="tumblr",
            title="Example title",
            artist="Example artist",
            album="Example album",
            media=MEDIA["parsed"],
            poster=audio_block_with_poster[1][0].poster,
        )
    ],
    dominate.tags.section(
        dominate.tags.header(
            dominate.tags.div(
                dominate.tags.h3("Example title", cls="ab-title"),
                dominate.tags.h4("Example artist", cls="ab-artist"),
                dominate.tags.h4("Example album", cls="ab-album"),
                cls="ab-metadata",
            ),
            dominate.tags.img(
                src="https://media.tumblr.com/someimage.png",
                srcset="https://media.tumblr.com/someimage.png 540w",
                sizes="(max-width: 540px) 100vh, 540px",
                alt="Example title",
                cls="ab-poster",
            ),
            cls="ab-heading",
        ),
        dominate.tags.audio(MEDIA["formatted"], controls=True),
        cls="ap-container",
    ),
)


audio_block_embed_spotify_test = (
    {
        "type": "audio",
        "provider": "spotify",
        "url": "https://open.spotify.com/track/FakeTrack",
        "title": "An example track",
        "artist": "A spotify artist",
        "album": "A collection of tracks",
        "embedUrl": "https://open.spotify.com/embed?uri=https%3A%2F%2Fopen.spotify.com%2Ftrack%2FFakeTrack&amp;view=coverart",
        "embedHtml": '<iframe class="spotify_audio_player" src="https://open.spotify.com/embed?uri=https%3A%2F%2Fopen.spotify.com%2Ftrack%2FFakeTrack&amp;view=coverart" frameborder="0" allowtransparency="true" width="500" height="580"></iframe>',
    },
    [
        objects.audio_block.AudioBlock(
            url="https://open.spotify.com/track/FakeTrack",
            provider="spotify",
            title="An example track",
            artist="A spotify artist",
            album="A collection of tracks",
            embed_url="https://open.spotify.com/embed?uri=https%3A%2F%2Fopen.spotify.com%2Ftrack%2FFakeTrack&amp;view=coverart",
            embed_html='<iframe class="spotify_audio_player" src="https://open.spotify.com/embed?uri=https%3A%2F%2Fopen.spotify.com%2Ftrack%2FFakeTrack&amp;view=coverart" frameborder="0" allowtransparency="true" width="500" height="580"></iframe>',
        )
    ],
    dominate.util.raw(
        '<iframe class="spotify_audio_player" src="https://open.spotify.com/embed?uri=https%3A%2F%2Fopen.spotify.com%2Ftrack%2FFakeTrack&amp;view=coverart" frameborder="0" allowtransparency="true" width="500" height="580"></iframe>'
    ),
)


forbid_external_iframes_fallback_test = (
    audio_block_embed_spotify_test[0],
    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.a(
                dominate.tags.div(dominate.tags.span("Embeds are disabled"), cls="link-block-title"),
                dominate.tags.div(
                    dominate.tags.p("Please click me to listen on the original site", cls="link-block-description"),
                    dominate.tags.div(dominate.tags.span(dominate.tags.span("spotify")), cls="link-block-subtitles"),
                    cls="link-block-description-container",
                ),
                href="https://open.spotify.com/track/FakeTrack",
                cls="link-block-link",
            ),
            cls="link-block",
        ),
        cls="post-body",
    ),
)


audio_block_with_tumblr_as_provider_but_non_tumblr_media_link = (
    {
        "type": "audio",
        "provider": "tumblr",
        "url": "https://on.soundcloud.com/fwehiufweouij",
        "media": {"url": "https://on.soundcloud.com/fwehiufweouij"},
    },
    [
        objects.audio_block.AudioBlock(
            url="https://on.soundcloud.com/fwehiufweouij",
            provider="tumblr",
            media=[
                objects.media_objects.MediaObject(
                    url="https://on.soundcloud.com/fwehiufweouij",
                    width=540,
                    height=405,
                )
            ],
        )
    ],
    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.a(
                dominate.tags.div(dominate.tags.span("Error: non-tumblr source for audio player"), cls="link-block-title"),
                dominate.tags.div(
                    dominate.tags.p("Please click me to listen on the original site", cls="link-block-description"),
                    dominate.tags.div(
                        dominate.tags.span(dominate.tags.span("on.soundcloud.com")), cls="link-block-subtitles"
                    ),
                    cls="link-block-description-container",
                ),
                href="https://on.soundcloud.com/fwehiufweouij",
                cls="link-block-link",
            ),
            cls="link-block",
        ),
        cls="post-body",
    ),
)

audio_block_fallbacks_to_link_block = (
    {
        "type": "audio",
        "url": "https://a.tumblr.com/someaudiosource.mp3",
    },
    [
        objects.audio_block.AudioBlock(
            url="https://a.tumblr.com/someaudiosource.mp3",
        )
    ],
    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.a(
                dominate.tags.div(dominate.tags.span("Error: unable to render audio block"), cls="link-block-title"),
                dominate.tags.div(
                    dominate.tags.p("Please click me to listen on the original site", cls="link-block-description"),
                    dominate.tags.div(
                        dominate.tags.span(dominate.tags.span("a.tumblr.com")), cls="link-block-subtitles"
                    ),
                    cls="link-block-description-container",
                ),
                href="https://a.tumblr.com/someaudiosource.mp3",
                cls="link-block-link",
            ),
            cls="link-block",
        ),
        cls="post-body",
    ),
)


audio_block_fallback_with_only_media_url_and_provider = (
    {"type": "audio", "provider": "tumblr", "media": {"url": "https://on.soundcloud.com/medialink"}},
    [
        objects.audio_block.AudioBlock(
            provider="tumblr",
            media=[objects.media_objects.MediaObject(url="https://on.soundcloud.com/medialink", width=540, height=405)],
        )
    ],
    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.a(
                dominate.tags.div(dominate.tags.span("Error: non-tumblr source for audio player"), cls="link-block-title"),
                dominate.tags.div(
                    dominate.tags.p("Please click me to listen on the original site", cls="link-block-description"),
                    dominate.tags.div(
                        dominate.tags.span(dominate.tags.span("on.soundcloud.com")), cls="link-block-subtitles"
                    ),
                    cls="link-block-description-container",
                ),
                href="https://on.soundcloud.com/medialink",
                cls="link-block-link",
            ),
            cls="link-block",
        ),
        cls="post-body",
    ),
)


audio_block_raises_when_all_else_fails = (
    {
        "type": "audio",
    },
    [objects.audio_block.AudioBlock()],
)
