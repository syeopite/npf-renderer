from example_text_block_data import *
from npf_renderer.parse.parse import Parser

import logging

try:
    import prettyprinter
    pprinter = prettyprinter.PrettyPrinter()
except ImportError:
    pprinter = None


def helper_function(raw, answer):
    parser = Parser(raw["content"])
    parsed_results = parser.parse()

    if pprinter:
        parsed_results = prettyprinter.pformat(parsed_results)
        answer = prettyprinter.pformat(answer)

    logging.info(f"Parsed: {parsed_results}")
    logging.info(f"Answer: {answer}")

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


def test_mixed_block_quote_list_parse():
    helper_function(mixed_block_quote_list_test[0], mixed_block_quote_list_test[1])


def test_top_level_list_with_children_merging_parse():
    helper_function(top_level_list_with_children_merging_test_data[0],
                    top_level_list_with_children_merging_test_data[1])