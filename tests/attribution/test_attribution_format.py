import logging

from npf_renderer.parse import misc
from npf_renderer.format import attribution as formatter

import attribution_test_data


def helper_function(raw, answer, url_handler=None):
    attribution = misc.parse_attribution(raw)

    if not url_handler:

        def url_handler(url):
            return url

    match attribution:
        case misc.attribution.BlogAttribution():
            formatted_results = formatter.format_blog_attribution(attribution, url_handler=url_handler)
        case misc.attribution.AppAttribution():
            formatted_results = formatter.format_app_attribution(attribution, url_handler)
        case misc.attribution.LinkAttribution():
            formatted_results = formatter.format_link_attribution(attribution, url_handler)
        case misc.attribution.PostAttribution():
            formatted_results = formatter.format_post_attribution(attribution, url_handler)
        case _:
            formatted_results = formatter.format_unsupported_attribution(attribution)

    logging.info(f"Formatted: {formatted_results}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_results) == str(answer)


def test_link_attribution_format():
    helper_function(attribution_test_data.link_attribution[0], attribution_test_data.link_attribution[2])


def test_post_attribution_format():
    helper_function(attribution_test_data.post_attribution[0], attribution_test_data.post_attribution[2])


def test_blog_attribution_format():
    helper_function(attribution_test_data.blog_attribution[0], attribution_test_data.blog_attribution[2])


def test_app_attribution_format():
    helper_function(attribution_test_data.app_attribution[0], attribution_test_data.app_attribution[2])


def test_unknown_attribution_format():
    helper_function(attribution_test_data.unsupported_attribution[0], attribution_test_data.unsupported_attribution[2])
