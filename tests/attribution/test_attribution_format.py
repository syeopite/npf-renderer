import logging

from npf_renderer.parse import misc
from npf_renderer.format import attribution as formatter

import attribution_test_data


def helper_function(raw, answer, url_handler=None):
    parsed_results = misc.parse_attribution(raw)

    if not url_handler:
        def url_handler(url):
            return url

    match parsed_results:
        case misc.attribution.BlogAttribution():
            formatted_results = formatter.format_blog_attribution(parsed_results, url_handler)
        # case misc.attribution.AppAttribution:
        #     pass
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