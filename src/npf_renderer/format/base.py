import functools

import dominate.tags

from . import text_formatter, image_formatter
from .. import objects, helpers


def _count_nested(block):
    count = len(block.nest)

    for nested in block.nest:
        if nested.nest:
            count += _count_nested(nested)

    return count


class Formatter(helpers.CursorIterator):
    def __init__(self, content, layout=None, trails=None, url_handler=None):
        """Initializes the parser with a list of content blocks (json objects) to parse"""
        super().__init__(content)

        if not url_handler:
            def url_handler(url):
                return url

        self.layout = layout
        self.current_context_padding = 0
        self.render_instructions = []

        self.url_handler = url_handler

        self.post = dominate.tags.div(cls="post")

    def _format_text(self, block):
        """Formats TextBlock(s) into usable HTML code"""
        formatted_block = text_formatter.TextFormatter(block, url_handler=self.url_handler).format()
        return formatted_block

    def _format_list(self, block):
        """Formats a ListGrouping of TextBlock(s) into an HTML list of its corresponding type"""
        if block.type == objects.text_block.Subtypes.ORDERED_LIST_ITEM:
            list_tag = dominate.tags.ol(cls="ordered-list")
        else:
            list_tag = dominate.tags.ul(cls="unordered-list")

        for blk in block.group:
            list_tag.add(self._format_text(blk))

        return list_tag

    @staticmethod
    def _format_image(block, row_length=1):
        """Renders an ImageBlock into HTML"""
        figure = dominate.tags.figure(cls="image-block")
        figure.add(image_formatter.format_image(block, row_length))

        if block.caption:
            figure.add(dominate.tags.figcaption(block.caption, cls="image-caption"))

        return figure

    def __prepare_instruction_for_current_block(self):
        """Finds and returns the instruction (method) necessary to render a content block"""
        match self.current:
            case objects.text_block.TextBlock():
                if self.current.nest:
                    self.current_context_padding = _count_nested(self.current)
                return self._format_text, (self.current,)
            case objects.text_block.ListGrouping():
                self.current_context_padding = len(self.current.group)
                return self._format_list, (self.current,)
            case objects.image.ImageBlock():
                return self._format_image, (self.current,)
            case _:  # Unreachable
                raise RuntimeError

    def _pad(self):
        [self.render_instructions.append(None) for _ in range(self.current_context_padding)]
        self.current_context_padding = 0

    def format(self):
        """Renders the list of content blocks into HTML"""

        while self.next():
            instruction = self.__prepare_instruction_for_current_block()
            self.render_instructions.append(instruction)
            self._pad()

        if self.layout:
            for layout in self.layout:
                if isinstance(layout, objects.layouts.Rows):
                    for row in layout.rows:
                        row_items = []
                        for index in row.ranges:
                            render_instructions = self.render_instructions[index]
                            if not render_instructions:
                                continue

                            render_method, arguments = render_instructions

                            match render_method:
                                case self._format_image:
                                    row_items.append(render_method(*arguments, len(row.ranges)))
                                case _:
                                    row_items.append(render_method(*arguments))

                        if not row_items:
                            continue

                        row_tag = dominate.tags.div(cls="layout-row")
                        self.post.add(row_tag)

                        [row_tag.add(i) for i in row_items]
        else:
            for render_instructions in self.render_instructions:
                if not render_instructions:
                    continue

                func, args = render_instructions
                self.post.add(func(*args))

        return self.post


def format_content(parsed_contents, layouts=None, trails=None, url_handler=None):
    return Formatter(parsed_contents, layouts, url_handler=url_handler).format()

