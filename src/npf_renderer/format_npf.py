from .format import format_content
from .parse import Parser, LayoutParser
from . import exceptions


def format_npf(contents, layouts=None, url_handler=None):
    contents = Parser(contents).parse()
    if layouts:
        layouts = LayoutParser(layouts).parse()

    try:
        contains_render_errors = False
        formatted = format_content(contents, layouts, url_handler)
    except exceptions.RenderErrorDisclaimerError as e:
        contains_render_errors = True
        formatted = e.rendered_result
        assert formatted is not None

    return contains_render_errors, formatted
