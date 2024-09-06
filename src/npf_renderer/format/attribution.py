import urllib.parse
from typing import Callable

import dominate.tags

from .. import objects


def format_link_attribution(attr: objects.attribution.LinkAttribution, url_handler: Callable):
    return dominate.tags.div(
        dominate.tags.a(
            urllib.parse.urlparse(attr.url).hostname,
            href=url_handler(attr.url),
        ),
        cls="link-attribution",
    )


def format_post_attribution(attr: objects.attribution.PostAttribution, url_handler: Callable):
    return dominate.tags.div(
        dominate.tags.a(
            f"From ",
            dominate.tags.b(attr.blog.name),
            href=url_handler(attr.url),
        ),
        cls="post-attribution",
    )


def format_blog_attribution(attr: objects.attribution.BlogAttribution, url_handler: Callable):
    return dominate.tags.div(
        dominate.tags.a(
            f"Created by ",
            dominate.tags.b(attr.name or "Anonymous"),
            href=url_handler(attr.url),
        ),
        cls="blog-attribution",
    )


def format_app_attribution(attr: objects.attribution.AppAttribution, url_handler: Callable):
    return dominate.tags.div(
        dominate.tags.a(
            f"View on ",
            dominate.tags.b(attr.app_name),
            href=url_handler(attr.url),
        ),
        cls="post-attribution",
    )


def format_unsupported_attribution(attr: objects.attribution.UnsupportedAttribution):
    return dominate.tags.div(
        dominate.tags.p(
            f"Attributed via unsupported '{attr.type_}' attribution type. Please report me.",
        ),
        cls="unknown-attribution",
    )


# See misc.format_ask()
# -------
# def format_ask_attribution():
#   pass
