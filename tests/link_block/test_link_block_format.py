import logging

from npf_renderer import format_npf

from example_link_block_data import *

def helper_function(raw, answer):
    has_error, formatted_result = format_npf(raw["content"])

    assert not has_error

    logging.info(f"Formatted: {formatted_result}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_result) == str(answer)


def test_simple_link_block_format():
    helper_function(simple_link_block[0], simple_link_block[2])


def test_link_block_with_title_format():
    helper_function(link_block_with_title[0], link_block_with_title[2])


def test_link_block_with_description_format():
    helper_function(link_block_with_description[0], link_block_with_description[2])


def test_link_block_with_title_and_description_format():
    helper_function(link_block_with_title_and_description[0], link_block_with_title_and_description[2])


def test_link_block_with_site_name_format():
    helper_function(link_block_with_site_name[0], link_block_with_site_name[2])


def test_link_block_with_site_name_and_author_format():
    helper_function(link_block_with_site_name_and_author[0], link_block_with_site_name_and_author[2])


def test_link_block_with_poster_format():
    helper_function(link_block_with_poster[0], link_block_with_poster[2])


def test_link_block_with_all_format():
    helper_function(link_block_with_all[0], link_block_with_all[2])
