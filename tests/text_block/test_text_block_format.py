import urllib.parse
import logging

from npf_renderer import format_npf

from example_text_block_data import *


def helper_function(content, answer):
    has_error, formatted_result = format_npf(content["content"])

    assert not has_error

    logging.info(f"Formatted: \n{formatted_result}\n")
    logging.info(f"Answer: \n{answer}\n")

    assert str(formatted_result) == str(answer)


def test_simple_text_render():
    helper_function(simple_test[0], simple_test[2])


def test_empty_string_render():
    helper_function(longer_and_with_empty_string_test[0], longer_and_with_empty_string_test[2])


def test_subtype_string_render():
    helper_function(subtype_string_test[0], subtype_string_test[2])


def test_subtype_string_render_2():
    helper_function(subtype_string_test_2[0], subtype_string_test_2[2])


def test_subtype_and_indent_level_render():
    helper_function(subtype_and_indent_level_test[0], subtype_and_indent_level_test[2])


def test_top_level_list_with_children_merging():
    helper_function(top_level_list_with_children_merging_test_data[0],
                    top_level_list_with_children_merging_test_data[2])

