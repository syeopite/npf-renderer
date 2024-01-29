import logging

from npf_renderer.parse.parse import Parser

import mock_audio_blocks

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
        answer = prettyprinter.pformat(answer)

    logging.info(f"Parsed: {parsed_results}")
    logging.info(f"Answer: {answer}")

    assert parsed_results == answer

def test_can_parse_basic_audio_block():
    return helper_function(mock_audio_blocks.basic_audio_block[0], mock_audio_blocks.basic_audio_block[1])


def test_can_parse_audio_block_with_title():
    return helper_function(mock_audio_blocks.audio_block_with_title[0], mock_audio_blocks.audio_block_with_title[1])


def test_can_parse_audio_block_with_metadata():
    return helper_function(mock_audio_blocks.audio_block_with_metadata[0], mock_audio_blocks.audio_block_with_metadata[1])


def test_can_parse_audio_block_with_poster():
    return helper_function(mock_audio_blocks.audio_block_with_poster[0], mock_audio_blocks.audio_block_with_poster[1])


def test_can_parse_audio_block_with_metadata_and_poster():
    return helper_function(mock_audio_blocks.audio_block_with_metadata_and_poster[0], mock_audio_blocks.audio_block_with_metadata_and_poster[1])


def test_can_parse_embedded_audio_block():
    return helper_function(mock_audio_blocks.audio_block_embed_spotify_test[0], mock_audio_blocks.audio_block_embed_spotify_test[1])


# def test_can_parse_external_embedded_but_with_media_object_audio_block():
#     return helper_function(mock_audio_blocks.audio_block_external_embed_but_with_media_object[0], mock_audio_blocks.audio_block_external_embed_but_with_media_object[1])
