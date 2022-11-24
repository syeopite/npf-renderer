from typing import Callable

import dominate.tags

from ..objects import attribution


def format_link_attribution(attr: attribution.LinkAttribution, url_handler: Callable):
    return dominate.tags.div(
        dominate.tags.a(
            href=url_handler(attr.url),
        ),
        cls="link-attribution"
    )

