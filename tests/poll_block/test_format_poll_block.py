import logging
import datetime

import dominate
from freezegun import freeze_time

from npf_renderer import format_npf
import mock_poll_blocks

def helper_function(raw, answer, callback = None):
    has_error, formatted_result = format_npf((raw,), pretty_html=True, poll_result_callback=callback)

    assert not has_error

    answer = dominate.tags.div(answer, cls="post-body")

    logging.info(f"Formatted: {formatted_result}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_result) == str(answer)


@freeze_time("2024-01-25 00:00:00")
def test_basic_expired_poll_block():
    return helper_function(mock_poll_blocks.simple_poll_expired[0], mock_poll_blocks.simple_poll_expired[2])


@freeze_time("2024-01-25 00:00:00")
def test_basic_expired_poll_block_with_results():
    return helper_function(
        mock_poll_blocks.simple_poll_expired[0],
        mock_poll_blocks.simple_poll_expired[3],
        callback=lambda _ : mock_poll_blocks.basic_poll_data[2]
    )


@freeze_time("2023-01-01 00:00:00")
def test_basic_ongoing_poll_block():
    return helper_function(mock_poll_blocks.simple_ongoing_poll[0], mock_poll_blocks.simple_ongoing_poll[2])


@freeze_time("2023-01-01 00:00:00")
def test_basic_ongoing_poll_block_with_results():
    return helper_function(
        mock_poll_blocks.simple_ongoing_poll[0],
        mock_poll_blocks.simple_ongoing_poll[3],
        callback=lambda _ : mock_poll_blocks.basic_poll_data[2]
    )


@freeze_time("2024-01-25 00:00:00")
def test_poll_with_a_extra_choice_without_any_results_attached():
    return helper_function(
        mock_poll_blocks.poll_with_extra_choice_without_any_results_attached[0], 
        mock_poll_blocks.poll_with_extra_choice_without_any_results_attached[2],
        callback=lambda _ : mock_poll_blocks.basic_poll_data[2]
    )


@freeze_time("2024-01-25 00:00:00")
def test_tied_poll():
    return helper_function(
        mock_poll_blocks.mock_tied_poll[0],
        mock_poll_blocks.mock_tied_poll[3],
        callback=lambda _ : mock_poll_blocks.mock_tied_poll[2]
    )

@freeze_time("2024-01-25 00:00:00")
def test_multiple_winners_poll():
    return helper_function(
        mock_poll_blocks.mock_multiple_winners_poll[0],
        mock_poll_blocks.mock_multiple_winners_poll[3],
        callback=lambda _ : mock_poll_blocks.mock_multiple_winners_poll[2]
    )