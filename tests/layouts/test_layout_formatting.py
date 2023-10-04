import logging

from npf_renderer import format_npf

import example_layout_data as data


def helper_function(raw, answer, contents_list = data.content_list):
    print(f"Contents: #{len(contents_list)}")

    has_error, formatted_result = format_npf(contents_list, raw["layouts"], pretty_html=True)

    assert not has_error

    logging.info(f"Formatted: {formatted_result}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_result) == str(answer)


def test_basic_layout_format():
    helper_function(data.basic_rows_layout_example[0], data.basic_rows_layout_example[2])


def test_ask_layout_format():
    helper_function(data.layouts_with_ask_section[0], data.layouts_with_ask_section[2])


def test_layouts_with_only_ask_section_format():
    helper_function(data.layouts_with_only_ask_section[0], data.layouts_with_only_ask_section[2])


def test_layouts_layouts_with_anon_ask_section_format():
    helper_function(data.layouts_with_anon_ask_section[0], data.layouts_with_anon_ask_section[2])


def test_layouts_in_content_with_lists_format():
    helper_function(data.layouts_in_content_with_lists[0], data.layouts_in_content_with_lists[2], data.with_list_content_list)
