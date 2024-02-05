import logging

from npf_renderer.parse.parse import Parser

import mock_poll_blocks

try:
    import prettyprinter
    pprinter = prettyprinter.PrettyPrinter()
except ImportError:
    pprinter = None


def helper_function(raw, answer, callback = None):
    parser = Parser((raw,), poll_result_callback=callback)
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


def test_poll_with_a_extra_choice_without_any_results_attached():
    return helper_function(mock_poll_blocks.poll_with_extra_choice_without_any_results_attached[0], mock_poll_blocks.poll_with_extra_choice_without_any_results_attached[1])


def test_tied_poll():
    return helper_function(
        mock_poll_blocks.mock_tied_poll[0],
        mock_poll_blocks.mock_tied_poll[1],
        callback=lambda _ : mock_poll_blocks.mock_tied_poll[2]
    )


def test_multiple_winners_poll():
    return helper_function(
        mock_poll_blocks.mock_multiple_winners_poll[0],
        mock_poll_blocks.mock_multiple_winners_poll[1],
        callback=lambda _ : mock_poll_blocks.mock_multiple_winners_poll[2]
    )