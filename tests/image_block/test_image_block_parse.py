import logging

from npf_renderer.parse.parse import Parser

import image_block_test_data as test_data

try:
    import prettyprinter

    pprinter = prettyprinter.PrettyPrinter()
except ImportError:
    pprinter = None


def helper_function(raw, answer):
    parser = Parser(raw)
    parsed_results = parser.parse()

    if pprinter:
        parsed_results = prettyprinter.pformat(parsed_results)
        answer = prettyprinter.pformat(answer)

    logging.info(f"Parsed: {parsed_results}")
    logging.info(f"Answer: {answer}")

    assert parsed_results == answer


def test_basic_image_block_parse():
    helper_function(test_data.basic_image_block[0], test_data.basic_image_block[1])


def test_gif_image_block_parse():
    helper_function(test_data.basic_gif_image_block[0], test_data.basic_gif_image_block[1])


def test_image_block_with_color_attr_parse():
    helper_function(test_data.image_block_with_color_attr[0], test_data.image_block_with_color_attr[1])


def test_gif_image_block_with_poster_parse():
    helper_function(test_data.gif_image_block_with_poster[0], test_data.gif_image_block_with_poster[1])


def test_gif_image_block_with_link_attribution():
    helper_function(
        test_data.gif_image_block_with_link_attribution[0], test_data.gif_image_block_with_link_attribution[1]
    )


def test_gif_image_block_with_post_attribution():
    helper_function(
        test_data.gif_image_block_with_post_attribution[0], test_data.gif_image_block_with_post_attribution[1]
    )


def test_image_block_with_app_attribution():
    helper_function(test_data.image_block_with_app_attribution[0], test_data.image_block_with_app_attribution[1])


def test_image_block_with_blog_attribution():
    helper_function(
        test_data.image_block_with_blog_attribution[0], test_data.image_block_with_blog_attribution[1]
    )


def test_image_block_with_unknown_attribution():
    helper_function(
        test_data.image_block_with_unknown_attribution[0], test_data.image_block_with_unknown_attribution[1]
    )
