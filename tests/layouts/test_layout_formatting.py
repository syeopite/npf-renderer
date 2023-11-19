import logging

from npf_renderer import format_npf

import example_layout_data as data


def helper_function(raw, answer, contents_list = data.content_list):
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


def test_with_nested_blocks_format():
    helper_function(data.with_nested_blocks_layout_list[0], data.with_nested_blocks_layout_list[2], data.with_nested_blocks_content_list)


def test_with_nested_list_blocks_format():
    helper_function(data.with_nested_list_blocks_layout_list[0], data.with_nested_list_blocks_layout_list[2], data.with_nested_list_blocks_content_list)


def test_reserve_image_space_layout_format():
    has_error, formatted_result = format_npf(
        data.reserve_image_space_content_list,
        data.reserve_image_space_layouts[0]["layouts"],
        pretty_html=True,
        skip_cropped_images=True,
        reserve_space_for_images=True
    )

    assert not has_error

    logging.info(f"Formatted: {formatted_result}")
    logging.info(f"Answer: {data.reserve_image_space_layouts[1]}")

    assert str(formatted_result) == str(data.reserve_image_space_layouts[1])