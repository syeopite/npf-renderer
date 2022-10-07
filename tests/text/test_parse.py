from example_data import *
from npf_renderer.parse.parse import Parser

import logging

import pprint
printer = pprint.PrettyPrinter(indent=4)


def helper_function(raw, answer):
    parser = Parser(raw["content"])
    parsed_results = parser.parse()
    logging.info(f"Parsed: {parsed_results}")

    assert parsed_results == answer


def test_simple_text_parse():
    helper_function(simple_test[0], simple_test[1])


def test_empty_string_parse():
    helper_function(longer_and_with_empty_string_test[0], longer_and_with_empty_string_test[1])

def test_subtype_string_parse():
    helper_function(subtype_string_test[0], subtype_string_test[1])


def test_subtype_string_parse_2():
    helper_function(subtype_string_test_2[0], subtype_string_test_2[1])


def test_subtype_and_indent_level_parse():
    helper_function(subtype_and_indent_level_test[0], subtype_and_indent_level_test[1])


def test_inline_formatting_parse():
    helper_function(inline_formatting_test[0], inline_formatting_test[1])


def test_inline_link_formatting_parse():
    helper_function(inline_formatting_link_test[0], inline_formatting_link_test[1])


def test_inline_mention_formatting_parse():
    helper_function(inline_formatting_mention_test[0], inline_formatting_mention_test[1])


def test_inline_color_formatting_parse():
    helper_function(inline_formatting_color_test[0], inline_formatting_color_test[1])


def test_overlapping_inline_parse():
    helper_function(test_inline_overlapping[0], test_inline_overlapping[1])
