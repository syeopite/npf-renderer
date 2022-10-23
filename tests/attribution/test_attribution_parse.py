import logging


from npf_renderer.parse import misc
import attribution_test_data


def helper_function(raw, answer):
    parsed_results = misc.parse_attribution(raw)

    logging.info(f"Parsed: {parsed_results}")
    logging.info(f"Answer: {answer}")

    assert parsed_results == answer


def test_blog_attribution():
    helper_function(attribution_test_data.blog_attribution[0], attribution_test_data.blog_attribution[1])


def test_post_attribution():
    helper_function(attribution_test_data.post_attribution[0], attribution_test_data.post_attribution[1])


def test_link_attribution():
    helper_function(attribution_test_data.link_attribution[0], attribution_test_data.link_attribution[1])


def test_app_attribution():
    helper_function(attribution_test_data.app_attribution[0], attribution_test_data.app_attribution[1])
