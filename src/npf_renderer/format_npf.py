from .format import format_content
from .parse import Parser, LayoutParser


def format_npf(contents, layouts=None, trails=None, url_handler=None):
    contents = Parser(contents).parse()
    if layouts:
        layouts = LayoutParser(layouts).parse()

    return format_content(contents, layouts, trails, url_handler)
