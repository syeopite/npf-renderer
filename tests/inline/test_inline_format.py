import logging
import urllib.parse

from npf_renderer import format_npf

from inline_formatting_data import *
from format_only_inline_test_data import *


def helper_function(content, answer, url_handler=None):
    has_error, formatted_result = format_npf(content["content"], url_handler=url_handler, pretty_html=True)

    assert not has_error

    logging.info(f"Formatted: \n{formatted_result}\n")
    logging.info(f"Answer: \n{answer}\n")

    assert str(formatted_result) == str(answer)


def test_render():
    helper_function(standard_test[0], standard_test[2])


def test_link_formatting_render():
    helper_function(link_test[0], link_test[2])


def test_mention_formatting_render():
    helper_function(mention_test[0], mention_test[2])


def test_color_formatting_render():
    helper_function(color_test[0], color_test[2])


def test_overlapping_render():
    helper_function(test_overlapping[0], test_overlapping[2])


# Exclusive formatting tests below:
# -------------------------------------------------------------
#

def test_back_to_back_render():
    helper_function({"content": back_to_back_format_test[0]}, back_to_back_format_test[1])


def test_connected_back_to_back_inline():
    helper_function({"content": connected_back_to_back_format_test[0]}, connected_back_to_back_format_test[1])


def test_long_space_inbetween_render():
    helper_function({"content": long_space_in_between_format_test[0]}, long_space_in_between_format_test[1])


def test_second_has_lower_end_index():
    helper_function({"content": second_has_lower_end_index_test[0]}, second_has_lower_end_index_test[1])


def test_second_has_lower_end_index_2():
    helper_function({"content": second_has_lower_end_index_test_2[0]}, second_has_lower_end_index_test_2[1])


def test_overlapping_same_area():
    helper_function({"content": overlapping_same_area_test_data[0]}, overlapping_same_area_test_data[1])


def test_overlapping_same_start_different_end_data():
    helper_function({"content": overlapping_same_start_different_end_data[0]},
                    overlapping_same_start_different_end_data[1])


def test_interrupted_same_indices_overlapping():
    helper_function({"content": interrupted_same_indices_overlapping[0]}, interrupted_same_indices_overlapping[1])


def test_interrupted_overlap():
    helper_function({"content": interrupted_overlap_test[0]}, interrupted_overlap_test[1])


def test_interrupted_overlap_2():
    helper_function({"content": interrupted_overlap_test_2[0]}, interrupted_overlap_test_2[1])


def test_interrupted_overlap_3():
    helper_function({"content": interrupted_overlap_test_3[0]}, interrupted_overlap_test_3[1])


def test_interrupted_overlap_4():
    helper_function({"content": interrupted_overlap_test_4[0]}, interrupted_overlap_test_4[1])


def test_interrupted_overlap_5():
    helper_function({"content": interrupted_overlap_test_5[0]}, interrupted_overlap_test_5[1])


def test_interrupted_overlap_6():
    helper_function({"content": interrupted_overlap_test_6[0]}, interrupted_overlap_test_6[1])


def test_same_index_with_other_overlap():
    helper_function({"content": same_index_with_other_overlap_test[0]}, same_index_with_other_overlap_test[1])


def test_link_url_handler_normal():
    helper_function({"content": link_url_handler_test_data[0]}, link_url_handler_test_data[1])


def test_link_url_handler_replaced():
    def url_handler(url):
        url = urllib.parse.urlparse(url)

        if url.hostname.endswith("youtube.com"):
            return url._replace(netloc="redirect.invidious.io").geturl()
        elif url.hostname.endswith("twitter.com"):
            return url._replace(netloc="nitter.net").geturl()
        elif url.hostname.endswith("reddit.com"):
            return url._replace(netloc="libredd.it").geturl()

    helper_function({"content": link_url_handler_test_data[0]}, link_url_handler_test_data[2], url_handler=url_handler)