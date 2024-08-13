from example_link_block_data import *
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


def test_simple_link_block_parse():
    helper_function(simple_link_block[0], simple_link_block[1])


def test_link_block_with_title_parse():
    helper_function(link_block_with_title[0], link_block_with_title[1])


def test_link_block_with_description_parse():
    helper_function(link_block_with_description[0], link_block_with_description[1])


def test_link_block_with_title_and_description_parse():
    helper_function(link_block_with_title_and_description[0], link_block_with_title_and_description[1])


def test_link_block_with_site_name_parse():
    helper_function(link_block_with_site_name[0], link_block_with_site_name[1])


def test_link_block_with_site_name_and_author_parse():
    helper_function(link_block_with_site_name_and_author[0], link_block_with_site_name_and_author[1])


def test_link_block_with_poster_parse():
    helper_function(link_block_with_poster[0], link_block_with_poster[1])


def test_link_block_with_all_parse():
    helper_function(link_block_with_all[0], link_block_with_all[1])
