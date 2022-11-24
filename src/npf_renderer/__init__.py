from .format import format_content
from .parse import Parser


def format_npf(contents, layouts=None, trails=None, url_handler=None):
    parsed_contents = Parser(contents).parse()

    return format_content(parsed_contents, layouts, trails, url_handler)

