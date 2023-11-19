import dominate

from .format import Formatter
from .parse import Parser, LayoutParser
from . import exceptions


def format_npf(contents, layouts=None, *_, url_handler=None, pretty_html=False):
    contents = Parser(contents).parse()
    if layouts:
        layouts = LayoutParser(layouts).parse()

    try:
        contains_render_errors = False
        formatted = Formatter(contents, layouts, url_handler).format()
    except exceptions.RenderErrorDisclaimerError as e:
        contains_render_errors = True
        formatted = e.rendered_result
        assert formatted is not None
    except Exception as e:
        # TODO
        # Something had gone wrong block
        formatted = dominate.tags.div(cls="post-body")
        contains_render_errors = True

    return contains_render_errors, formatted.render(pretty=pretty_html)
