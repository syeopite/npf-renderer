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

    def __format_text(self):
        """Formats TextBlock(s) into usable HTML code"""
        formatted_block = text_formatter.TextFormatter(self.current, url_handler=self.url_handler).format()

        # We are currently at the zeroth level. And lists at the zeroth level
        # should be merged if they are next to each other and of the same type.
        if self.current.subtype in objects.text_block.ListsSubtype:
            while peekaboo := self.peek():
                if (not isinstance(peekaboo, objects.text_block.TextBlock)
                        or (peekaboo.subtype not in objects.text_block.ListsSubtype)):

                    return formatted_block

                if peekaboo.subtype == self.current.subtype:
                    # Formatted block should be a list element such as ul, ol here
                    self.next()
                    formatted_block.add(
                        text_formatter.TextFormatter(
                            self.current,
                            create_list_element=False,
                            url_handler=self.url_handler
                        ).format()
                    )

        return formatted_block

    def __format_block(self):
        """Formats a content block and adds it to the main post

        Works by routing specific content types to corresponding format methods
        """
        match self.current:
            case objects.text_block.TextBlock():
                block = self.__format_text()
                self.post.add(block)
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

