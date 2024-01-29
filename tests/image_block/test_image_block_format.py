import urllib.parse
import logging

from npf_renderer import format_npf

import image_block_test_data as test_data


def helper_function(raw, answer, **kwargs):
    has_error, formatted_result = format_npf(raw, pretty_html=True, **kwargs)

    assert not has_error

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


# Link replacing test
def test_image_block_url_replacement_format():
    def url_handler(url):
        url = urllib.parse.urlparse(url)

        if url.hostname.endswith("69.media.tumblr.com"):
            return url._replace(netloc="example.com").geturl()

    helper_function(test_data.image_block_with_replaced_link[0], test_data.image_block_with_replaced_link[2], url_handler=url_handler)


def test_gif_image_block_with_link_attribution_format():
    helper_function(test_data.gif_image_block_with_link_attribution[0],
                    test_data.gif_image_block_with_link_attribution[2])


def test_gif_image_block_with_post_attribution_format():
    helper_function(test_data.gif_image_block_with_post_attribution[0],
                    test_data.gif_image_block_with_post_attribution[2])


def test_image_block_with_app_attribution_format():
    helper_function(test_data.image_block_with_app_attribution[0], test_data.image_block_with_app_attribution[2])


def test_if_cropped_images_are_skipped():
    helper_function(test_data.skips_cropped_image_block_test[0], test_data.skips_cropped_image_block_test[1])


def test_reserve_space_for_images_parameter():
    helper_function(test_data.reserve_space_for_image_test[0], test_data.reserve_space_for_image_test[1], reserve_space_for_images=True)