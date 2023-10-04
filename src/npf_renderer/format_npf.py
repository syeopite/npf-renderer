from .format import Formatter
from .parse import Parser, LayoutParser
from . import exceptions


def format_npf(contents, layouts=None, url_handler=None, 
               parser=Parser, layout_parser=LayoutParser, formatter=Formatter, 
               pretty_html=False):
    contents = parser(contents).parse()
    if layouts:
        layouts = layout_parser(layouts).parse()

    try:
        contains_render_errors = False
        formatted = formatter(contents, layouts, url_handler).format()
    except exceptions.RenderErrorDisclaimerError as e:
        contains_render_errors = True
        formatted = e.rendered_result
        assert formatted is not None

    return contains_render_errors, formatted.render(pretty=pretty_html)
