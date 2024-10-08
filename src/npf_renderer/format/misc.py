from typing import Callable, Optional

import dominate.tags
import dominate.util

from ..objects import attribution


def format_ask(
    blog_attribution: Optional[attribution.BlogAttribution],
    *ask_contents: dominate.tags.dom_tag,
    url_handler: Callable = lambda url: url,
):
    """Renders an "ask" in HTML with the given data

    Args:
        blog_attribution:
            The attribution data for the sender of the ask.
            When none is provided the ask will be attributed to "Anonymous"
        *ask_contents:
            A sequential list of the asks's contents pre-rendered as HTML
        url_handler:
            A callable function used to process URLs.
            By default the URL remains unchanged.
    """
    if not blog_attribution:
        asker_attribution = dominate.tags.p(dominate.tags.strong("Anonymous", cls="asker-name"), " asked:", cls="asker")

        asker_avatar = dominate.tags.img(
            src=url_handler("https://assets.tumblr.com/images/anonymous_avatar_96.gif"),
            loading="lazy",
            cls="avatar asker-avatar image",
        )

    else:
        asker_attribution = dominate.tags.p(
            dominate.tags.a(
                dominate.tags.strong(blog_attribution.name, cls="asker-name"),
                href=url_handler(f"https://{blog_attribution.name}.tumblr.com/"),
                cls="asker-attribution",
            ),
            " asked:",
            cls="asker",
        )

        if blog_attribution.avatar:
            asker_avatar = dominate.tags.img(
                src=url_handler(blog_attribution.avatar[0].url), loading="lazy", cls="avatar asker-avatar image"
            )
        else:
            asker_avatar = None

    with dominate.tags.div(cls="ask") as ask:
        with dominate.tags.div(cls="ask-body"):
            with dominate.tags.div(cls="ask-header") as ask_header:
                ask_header.add(asker_attribution)

            with dominate.tags.div(cls="ask-content") as ask_content:
                for children in ask_contents:
                    ask_content.add(children)

    if asker_avatar:
        ask.add(asker_avatar)

    return ask
