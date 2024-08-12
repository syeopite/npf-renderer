import logging

from npf_renderer.parse.parse import Parser

import mocks

try:
    import prettyprinter

    pprinter = prettyprinter.PrettyPrinter()
except ImportError:
    pprinter = None


def helper_function(raw, answer):
    parser = Parser(raw)
    parsed_results = parser.parse()

    if pprinter:
        parsed_results = prettyprinter.pformat(parsed_results)
        answer = prettyprinter.pformat(answer)

    logging.info(f"Parsed: {parsed_results}")
    logging.info(f"Answer: {answer}")

    assert parsed_results == answer


def test_basic_video_parse():
    return helper_function(mocks.basic_video[0], mocks.basic_video[1])


def test_simplest_possible_video_parse():
    return helper_function(mocks.simplest_possible_video[0], mocks.simplest_possible_video[1])


def test_simple_embedded_arbitrary_video_parse():
    return helper_function(mocks.embedded_arbitrary_video[0], mocks.embedded_arbitrary_video[1])


def test_simple_embedded_youtube_video_format():
    return helper_function(mocks.embedded_youtube_video[0], mocks.embedded_youtube_video[1])


def test_video_block_fallbacks_to_link_block():
    return helper_function(mocks.video_block_fallbacks_to_link_block[0], mocks.video_block_fallbacks_to_link_block[1])


def test_video_block_fallbacks_to_link_block_when_invalid_media_source():
    return helper_function(
        mocks.video_block_fallbacks_to_link_block_when_invalid_media_source[0],
        mocks.video_block_fallbacks_to_link_block_when_invalid_media_source[1],
    )


def test_video_block_raises_when_all_else_fails():
    return helper_function(
        mocks.video_block_raises_when_all_else_fails[0], mocks.video_block_raises_when_all_else_fails[1]
    )
