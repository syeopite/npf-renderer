import logging

from npf_renderer.parse import misc
from npf_renderer.format import attribution as formatter
from npf_renderer.format.misc import format_ask

import attribution_test_data


def helper_function(raw, answer, url_handler=None):
    parsed_results = misc.parse_attribution(raw)

    if not url_handler:

        def url_handler(url):
            return url

    match parsed_results:
        case misc.attribution.BlogAttribution():
            formatted_results = format_ask(url_handler, blog_attribution=parsed_results)
        case misc.attribution.AppAttribution():
            formatted_results = formatter.format_app_attribution(parsed_results, url_handler)
        case misc.attribution.LinkAttribution():
            formatted_results = formatter.format_link_attribution(parsed_results, url_handler)
        case misc.attribution.PostAttribution():
            formatted_results = formatter.format_post_attribution(parsed_results, url_handler)
        case _:
            raise RuntimeError("Not possible")

    logging.info(f"Formatted: {formatted_results}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_results) == str(answer)


def test_link_attribution_format():
    helper_function(attribution_test_data.link_attribution[0], attribution_test_data.link_attribution[2])


def test_post_attribution_format():
    helper_function(attribution_test_data.post_attribution[0], attribution_test_data.post_attribution[2])


# More of an ask layouts test than blog attribution.
def test_blog_attribution_format():
    helper_function(attribution_test_data.blog_attribution[0], attribution_test_data.blog_attribution[2])


def test_app_attribution_format():
    helper_function(attribution_test_data.app_attribution[0], attribution_test_data.app_attribution[2])
