import logging
import dominate

from npf_renderer import format_npf

import mock_audio_blocks

def helper_function(raw, answer, forbid_external_iframes=False):
    has_error, formatted_result = format_npf(
        (raw,), 
        pretty_html=True, 
        forbid_external_iframes=forbid_external_iframes
    )

    assert not has_error

    answer = dominate.tags.div(dominate.tags.div(answer, cls="audio-block"), cls="post-body")

    logging.info(f"Formatted: {formatted_result}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_result) == str(answer)


def test_can_format_basic_audio_block():
    return helper_function(mock_audio_blocks.basic_audio_block[0], mock_audio_blocks.basic_audio_block[2])


def test_can_format_audio_block_with_title():
    return helper_function(mock_audio_blocks.audio_block_with_title[0], mock_audio_blocks.audio_block_with_title[2])


def test_can_format_audio_block_with_metadata():
    return helper_function(mock_audio_blocks.audio_block_with_metadata[0], mock_audio_blocks.audio_block_with_metadata[2])


def test_can_format_audio_block_with_poster():
    return helper_function(mock_audio_blocks.audio_block_with_poster[0], mock_audio_blocks.audio_block_with_poster[2])


def test_can_format_audio_block_with_metadata_and_poster():
    return helper_function(mock_audio_blocks.audio_block_with_metadata_and_poster[0], mock_audio_blocks.audio_block_with_metadata_and_poster[2])


def test_can_format_embedded_audio_block():
    return helper_function(mock_audio_blocks.audio_block_embed_spotify_test[0], mock_audio_blocks.audio_block_embed_spotify_test[2])


# def test_external_source_with_media_data_can_use_native_audio_player():
#     return helper_function(mock_audio_blocks.audio_block_external_embed_but_with_media_object[0], mock_audio_blocks.audio_block_external_embed_but_with_media_object[2])


# def test_can_format_exclude_external_sources():
#     # When external media sources are excluded the below should just return the embed iframe HTML
#     return helper_function(
#         mock_audio_blocks.audio_block_external_embed_but_with_media_object[0], 
#         dominate.util.raw(mock_audio_blocks.audio_block_external_embed_but_with_media_object[1][0].embed_html),
#         forbid_external_media_sources=True
#     )


def test_fallback_to_link_block_when_unable_to_format_audio_block():
    has_error, formatted_result = format_npf(
        (mock_audio_blocks.forbid_external_iframes_fallback_test[0],),
        pretty_html=True, 
        forbid_external_iframes=True
    )

    assert not has_error

    answer = mock_audio_blocks.forbid_external_iframes_fallback_test[1]

    logging.info(f"Formatted: {formatted_result}")
    logging.info(f"Answer: {answer}")

    assert str(formatted_result) == str(answer)
