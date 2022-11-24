import urllib.parse
from typing import Callable

import dominate.tags

from ..objects import attribution


def format_link_attribution(attr: attribution.LinkAttribution, url_handler: Callable):
    return dominate.tags.div(
        dominate.tags.a(
            urllib.parse.urlparse(attr.url).hostname,
            href=url_handler(attr.url),
        ),
        cls="link-attribution"
    )


def format_post_attribution(attr: attribution.PostAttribution, url_handler: Callable):
    return dominate.tags.div(
        dominate.tags.a(
            f"From ",
            dominate.tags.b(
                attr.blog.name
            ),
            href=url_handler(attr.url),
        ),
        cls="post-attribution"
    )
