import logging

from npf_renderer import parse, format

from example_data import *
from exclusive_formatting_test_data import *


def helper_function(content, answer):
    parsed_results = parse.Parser(content["content"]).parse()
    formatted_result = format.format_content(parsed_results)

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


def test_inline_formatting_render():
    helper_function(inline_formatting_test[0], inline_formatting_test[2])


def test_inline_link_formatting_render():
    helper_function(inline_formatting_link_test[0], inline_formatting_link_test[2])


def test_inline_mention_formatting_render():
    helper_function(inline_formatting_mention_test[0], inline_formatting_mention_test[2])


def test_inline_color_formatting_render():
    helper_function(inline_formatting_color_test[0], inline_formatting_color_test[2])


def test_overlapping_inline_render():
    helper_function(test_inline_overlapping[0], test_inline_overlapping[2])


# Exclusive formatting tests below:

def test_back_to_back_render():
    helper_function({"content": back_to_back_inline_format_test[0]}, back_to_back_inline_format_test[1])


def test_connected_back_to_back_inline():
    helper_function({"content": connected_back_to_back_inline_format_test[0]}, connected_back_to_back_inline_format_test[1])


def test_long_space_inbetween_render():
    helper_function({"content": long_space_in_between_format_test[0]}, long_space_in_between_format_test[1])

