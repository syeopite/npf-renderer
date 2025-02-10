import logging
import copy

import pytest
import dominate
from freezegun import freeze_time
from npf_renderer import format_npf, DEFAULT_LOCALIZATION

import i18n_test_data as mocks


def helper_function(content, answer, layouts=None, test_localizer={}, poll_callback=None):
    localizer = copy.copy(DEFAULT_LOCALIZATION)

    for localizer_type in localizer.keys():
        if localizer_type in test_localizer:
            localizer[localizer_type] = localizer[localizer_type] | test_localizer[localizer_type]

    has_error, formatted_result = format_npf(
        content, layouts, localizer=localizer, pretty_html=True, poll_result_callback=poll_callback
    )

    assert not has_error

    logging.info(f"Formatted: {formatted_result}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_result) == str(answer)


def test_can_modify_strings():
    helper_function(
        mocks.basic_string_modification["contents"],
        mocks.basic_string_modification["answer"],
        test_localizer=mocks.basic_string_modification["localizer"],
    )


def test_can_translate_strings_in_ask():
    helper_function(
        mocks.ask_i18n["contents"],
        mocks.ask_i18n["answer"],
        layouts=mocks.ask_i18n["layouts"],
        test_localizer=mocks.ask_i18n["localizer"],
    )


@freeze_time("2023-01-01 00:00:00")
@pytest.mark.parametrize("number,expected_plural", [(0, 0), (1, 1), (2, 2), (6, 3), (99, 4), (300, 5)])
def test_can_delgate_plurals(number, expected_plural):
    helper_function(
        content=mocks.can_format_plurals["contents"],
        answer=dominate.tags.div(mocks.generate_mock_poll_based_on_number(number, expected_plural), cls="post-body"),
        poll_callback=lambda _: mocks.generate_results_for_poll(number),
        test_localizer=mocks.can_format_plurals["localizer"],
    )


@freeze_time("2023-01-01 00:00:00")
def test_can_format_duration():
    helper_function(
        content=mocks.can_format_duration["contents"],
        answer=dominate.tags.div(
            mocks.generate_mock_poll_based_on_number(250, None, poll_footer=mocks.can_format_duration["poll_footer"]),
            cls="post-body",
        ),
        poll_callback=lambda _: mocks.generate_results_for_poll(250),
        test_localizer=mocks.can_format_duration["localizer"],
    )


@freeze_time("2024-01-01 00:00:00")
def test_can_format_datetime():
    helper_function(
        content=mocks.can_format_datetime["contents"],
        answer=dominate.tags.div(
            mocks.generate_mock_poll_based_on_number(
                250, None, poll_footer=mocks.can_format_datetime["poll_footer"], expired=True
            ),
            cls="post-body",
        ),
        poll_callback=lambda _: mocks.generate_results_for_poll(250),
        test_localizer=mocks.can_format_datetime["localizer"],
    )
