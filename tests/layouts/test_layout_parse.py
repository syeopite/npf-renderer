import logging

import example_layout_data as data
from npf_renderer.parse.layout_parse import LayoutParser

try:
    import prettyprinter

    pprinter = prettyprinter.PrettyPrinter()
except ImportError:
    pprinter = None


def helper_function(raw, answer):
    parsed_results = LayoutParser(raw["layouts"]).parse()

    if pprinter:
        parsed_results = prettyprinter.pformat(parsed_results)
        answer = prettyprinter.pformat(answer)

    logging.info(f"Parsed: {parsed_results}")
    logging.info(f"Answer: {answer}")

    assert parsed_results == answer


def test_basic_layout_parse():
    helper_function(data.basic_rows_layout_example[0], data.basic_rows_layout_example[1])


def test_basic_layout_with_truncate_parse():
    helper_function(data.basic_rows_layout_with_truncate_example[0], data.basic_rows_layout_with_truncate_example[1])


def test_rows_with_carousel_and_weighted_parse():
    helper_function(data.rows_with_carousel_and_weighted[0], data.rows_with_carousel_and_weighted[1])


def test_layouts_with_ask_section_parse():
    helper_function(data.layouts_with_ask_section[0], data.layouts_with_ask_section[1])


def test_layouts_with_only_ask_section_parse():
    helper_function(data.layouts_with_only_ask_section[0], data.layouts_with_only_ask_section[1])


def test_layouts_with_anon_ask_section_parse():
    helper_function(data.layouts_with_anon_ask_section[0], data.layouts_with_anon_ask_section[1])
