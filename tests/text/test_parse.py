from example_data import *
import hashlib
from npf_renderer.parse.text_block import TextBlockNPFParser
import logging


def helper_function(raw, answer_hash):
    parsed_results = []
    for block in raw["content"]:
        parsed_results.append(TextBlockNPFParser.process(block))

    hashed_result = hashlib.sha1(str(parsed_results).encode("utf-8")).hexdigest()

    logging.info(f"Parsed: {parsed_results}")
    logging.info(f"Hashed to: {hashed_result}")
    assert hashed_result == answer_hash


def test_simple_text_parse():
    helper_function(*simple_test)


def test_empty_string_parse():
    helper_function(*longer_and_with_empty_string_test)


def test_subtype_string_parse():
    helper_function(*subtype_string_test)


def test_subtype_string_parse_2():
    helper_function(*subtype_string_test_2)


def test_subtype_and_indent_level_parse():
    helper_function(*subtype_and_indent_level_test)


def test_inline_formatting_parse():
    helper_function(*inline_formatting_test)


def test_inline_link_formatting_parse():
    helper_function(*inline_formatting_link_test)


def test_inline_mention_formatting_parse():
    helper_function(*inline_formatting_mention_test)


def test_inline_color_formatting_parse():
    helper_function(*inline_formatting_color_test)


def test_overlapping_inline_parse():
    helper_function(*test_inline_overlapping)
