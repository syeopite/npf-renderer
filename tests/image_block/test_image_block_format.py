import logging

from npf_renderer.parse.parse import Parser
from npf_renderer import format

import image_block_test_data as test_data


def helper_function(raw, answer):
    parser = Parser(raw)
    parsed_results = parser.parse()

    formatted_result = format.format_content(parsed_results)

    logging.info(f"Formatted: {formatted_result}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_result) == str(answer)


def test_basic_image_block_format():
    helper_function(test_data.basic_image_block[0], test_data.basic_image_block[2])


def test_gif_image_block_format():
    helper_function(test_data.basic_gif_image_block[0], test_data.basic_gif_image_block[2])


# Pretty much just the same test as test_gif_image_block_format since we don't do anything with the color data
def test_image_block_with_color_attr_format():
    helper_function(test_data.image_block_with_color_attr[0], test_data.image_block_with_color_attr[2])


# Ditto except with poster data
def test_gif_image_block_with_poster_format():
    helper_function(test_data.gif_image_block_with_poster[0], test_data.gif_image_block_with_poster[2])

# TODO
#
# def test_gif_image_block_with_link_attribution_format():
#     helper_function(test_data.gif_image_block_with_link_attribution[0],
#                     test_data.gif_image_block_with_link_attribution[1])
#
#
# def test_gif_image_block_with_post_attribution_format():
#     helper_function(test_data.gif_image_block_with_post_attribution[0],
#                     test_data.gif_image_block_with_post_attribution[1])
#