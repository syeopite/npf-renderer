import logging

import dominate
from npf_renderer import format_npf, objects, parse

simple_unsupported_block = (
    [{"type": "some random block", "attributes": "value"}],
    [objects.unsupported.Unsupported("some random block")],
    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.h1("Unsupported NPF block"),
                dominate.tags.p(
                    'Placeholder for the unsupported "some random block" type NPF block. Please report me over at https://github.com/syeopite/npf-renderer'
                ),
                cls="unsupported-content-block-message",
            ),
            cls="unsupported-content-block",
        ),
        cls="post-body",
    ),
)


def helper_function(result, answer):
    try:
        import prettyprinter

        result = prettyprinter.pformat(result)
        answer = prettyprinter.pformat(answer)
    except ImportError:
        pass

    logging.info(f"Result: {result}")
    logging.info(f"Answer: {answer}")

    assert result == answer


def test_parse_unsupported_block():
    return helper_function(parse.Parser(simple_unsupported_block[0]).parse(), simple_unsupported_block[1])


def test_format_unsupported_block():
    _, results = format_npf(simple_unsupported_block[0], pretty_html=True)

    return helper_function(str(results), str(simple_unsupported_block[2]))
