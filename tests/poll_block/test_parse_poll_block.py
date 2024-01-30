import logging

from npf_renderer.parse.parse import Parser

import mock_poll_blocks

try:
    import prettyprinter
    pprinter = prettyprinter.PrettyPrinter()
except ImportError:
    pprinter = None


def helper_function(raw, answer):
    parser = Parser((raw,))
    parsed_results = parser.parse()

    if pprinter:
        parsed_results = prettyprinter.pformat(parsed_results)
        answer = prettyprinter.pformat([answer])

    logging.info(f"Parsed: {parsed_results}")
    logging.info(f"Answer: {answer}")

    assert parsed_results == answer

def test_basic_expired_poll_block():
    return helper_function(mock_poll_blocks.simple_poll_expired[0], mock_poll_blocks.simple_poll_expired[1])


def test_basic_ongoing_poll_block():
    return helper_function(mock_poll_blocks.simple_ongoing_poll[0], mock_poll_blocks.simple_ongoing_poll[1])
