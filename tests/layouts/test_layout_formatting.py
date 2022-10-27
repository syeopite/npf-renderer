import logging

import example_layout_data as data
from npf_renderer import parse

from npf_renderer.format.base import format_content


def helper_function(raw, answer):
    parsed_layouts = parse.LayoutParser(raw["layouts"]).parse()
    parsed_contents = parse.Parser(data.content_list).parse()

    formatted_results = format_content(parsed_contents, parsed_layouts)

    logging.info(f"Formatted: {formatted_results}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_results) == str(answer)


def test_basic_layout_format():
    helper_function(data.basic_rows_layout_example[0], data.basic_rows_layout_example[2])


