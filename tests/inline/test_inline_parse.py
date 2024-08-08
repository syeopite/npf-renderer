from inline_formatting_data import *
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


def test_parse():
    helper_function(standard_test[0], standard_test[1])


def test_link_formatting_parse():
    helper_function(link_test[0], link_test[1])


def test_mention_formatting_parse():
    helper_function(mention_test[0], mention_test[1])


def test_color_formatting_parse():
    helper_function(color_test[0], color_test[1])
