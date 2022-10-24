import logging

from npf_renderer.parse.parse import Parser

import image_block_test_data as test_data


def helper_function(raw, answer):
    parser = Parser(raw)
    parsed_results = parser.parse()

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
    helper_function(test_data.gif_image_block_with_link_attribution[0],
                    test_data.gif_image_block_with_link_attribution[1])


def test_gif_image_block_with_post_attribution():
    helper_function(test_data.gif_image_block_with_post_attribution[0],
                    test_data.gif_image_block_with_post_attribution[1])

