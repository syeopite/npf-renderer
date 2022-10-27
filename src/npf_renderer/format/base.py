import dominate.tags

from . import text_formatter, image_formatter
from .. import objects, helpers


class Formatter(helpers.CursorIterator):
    def __init__(self, content, layout=None, trails=None, url_handler=None):
        """Initializes the parser with a list of content blocks (json objects) to parse"""
        super().__init__(content)

        if not url_handler:
            def url_handler(url):
                return url

        self.post = dominate.tags.div(cls="post")
        self.url_handler = url_handler

    def __format_text(self, block):
        """Formats TextBlock(s) into usable HTML code"""
        formatted_block = text_formatter.TextFormatter(block, url_handler=self.url_handler).format()
        return formatted_block

    def __format_block(self):
        """Formats a content block and adds it to the main post

        Works by routing specific content types to corresponding format methods
        """
        match self.current:
            case objects.text_block.TextBlock():
                block = self.__format_text(self.current)
                self.post.add(block)
            case objects.text_block.ListGrouping():
                if self.current.type == objects.text_block.Subtypes.ORDERED_LIST_ITEM:
                    list_tag = dominate.tags.ol(cls="ordered-list")
                else:
                    list_tag = dominate.tags.ul(cls="unordered-list")

                for block in self.current.group:
                    list_tag.add(self.__format_text(block))

                self.post.add(list_tag)

            case objects.image.ImageBlock():
                figure = dominate.tags.figure(cls="image-block")
                figure.add(image_formatter.format_image(self.current))

                if self.current.caption:
                    figure.add(dominate.tags.figcaption(self.current.caption, cls="image-caption"))

                self.post.add(figure)

    def format(self):
        """Begins the parsing chain and returns the final list of parsed objects"""
        while self.next():
            self.__format_block()

        return self.post


def format_content(parsed_contents, layouts=None, trails=None, url_handler=None):
    return Formatter(parsed_contents, url_handler=url_handler).format()

