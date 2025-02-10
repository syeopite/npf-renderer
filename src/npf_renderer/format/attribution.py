import urllib.parse
from typing import Callable

import dominate.tags

from . import i18n
from .. import objects


def format_link_attribution(attr: objects.attribution.LinkAttribution, url_handler: Callable, localizer):
    return dominate.tags.div(
        dominate.tags.a(
            urllib.parse.urlparse(attr.url).hostname,
            href=url_handler(attr.url),
        ),
        cls="link-attribution",
    )


def format_post_attribution(attr: objects.attribution.PostAttribution, url_handler: Callable, localizer):
    return dominate.tags.div(
        dominate.tags.a(
            dominate.util.raw(
                i18n.translate(
                    localizer, "post_attribution", author=dominate.tags.b(attr.blog.name).render(pretty=False)
                )
            ),
            href=url_handler(attr.url),
        ),
        cls="post-attribution",
    )


def format_blog_attribution(attr: objects.attribution.BlogAttribution, url_handler: Callable, localizer):
    result = dominate.tags.div(
        dominate.tags.a(
            dominate.util.raw(
                i18n.translate(
                    localizer, "blog_attribution", author=dominate.tags.b(attr.name or "Anonymous").render(pretty=False)
                )
            ),
            href=url_handler(attr.url),
        ),
        cls="blog-attribution",
    )

    return result


def format_app_attribution(attr: objects.attribution.AppAttribution, url_handler: Callable, localizer):
    return dominate.tags.div(
        dominate.tags.a(
            dominate.util.raw(
                i18n.translate(
                    localizer, "app_attribution", platform=dominate.tags.b(attr.app_name).render(pretty=False)
                )
            ),
            href=url_handler(attr.url),
        ),
        cls="post-attribution",
    )


def format_unsupported_attribution(attr: objects.attribution.UnsupportedAttribution, localizer):
    return dominate.tags.div(
        dominate.tags.p(
            i18n.translate(localizer, "unsupported_attribution", attributee=attr.type_),
        ),
        cls="unknown-attribution",
    )


# See misc.format_ask()
# -------
# def format_ask_attribution():
#   pass
