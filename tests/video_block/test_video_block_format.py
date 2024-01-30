import logging

from npf_renderer import format_npf

import mocks

def helper_function(raw, answer, forbid_external_iframes=False):
    has_error, formatted_result = format_npf(raw, pretty_html=True, forbid_external_iframes=forbid_external_iframes)

    assert not has_error

    logging.info(f"Formatted: {formatted_result}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_result) == str(answer)


def test_basic_native_video_format():
    return helper_function(mocks.basic_video[0], mocks.basic_video[2])


def test_simplest_possible_video_format():
    return helper_function(mocks.simplest_possible_video[0], mocks.simplest_possible_video[2])


def test_simple_embedded_arbitrary_video_format():
    return helper_function(mocks.embedded_arbitrary_video[0], mocks.embedded_arbitrary_video[2])


def test_simple_embedded_youtube_video_format():
    return helper_function(mocks.embedded_youtube_video[0], mocks.embedded_youtube_video[2])


def test_embedded_forbid_external_iframes_fallback_format():
    return helper_function(mocks.embedded_forbid_external_iframes_fallback[0], mocks.embedded_forbid_external_iframes_fallback[2], forbid_external_iframes=True)


def test_video_block_fallbacks_to_link_block():
    return helper_function(mocks.video_block_fallbacks_to_link_block[0], mocks.video_block_fallbacks_to_link_block[2])


def test_video_block_fallbacks_to_link_block_when_invalid_media_source():
    return helper_function(mocks.video_block_fallbacks_to_link_block_when_invalid_media_source[0], mocks.video_block_fallbacks_to_link_block_when_invalid_media_source[2])


def test_video_block_raises_when_all_else_fails():
    has_error, _ = format_npf(mocks.video_block_raises_when_all_else_fails[0])
    assert has_error is True

