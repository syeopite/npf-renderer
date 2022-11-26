from .format import format_content
from .parse import Parser, LayoutParser


def format_npf(contents, layouts=None, trails=None, url_handler=None):
    parsed_contents = Parser(contents).parse()
    parsed_layouts = LayoutParser(layouts).parse()

    return format_content(parsed_contents, parsed_layouts, trails, url_handler)
