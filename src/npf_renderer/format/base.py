import dominate.tags

from . import text, image, misc
from .. import objects, helpers, exceptions


def _count_nested(block):
    count = len(block.nest)

    for nested in block.nest:
        if nested.nest:
            count += _count_nested(nested)

    return count


class Formatter(helpers.CursorIterator):
    def __init__(self, content, layout=None, url_handler=None):
        """Initializes the parser with a list of content blocks (json objects) to parse"""
        super().__init__(content)

        if not url_handler:
            def url_handler(url):
                return url

        self.layout = layout
        self.current_context_padding = 0
        self.render_instructions = []

        self.url_handler = url_handler

        self.has_render_error = False

        self.post = dominate.tags.div(cls="post-body")

    def _format_text(self, block):
        """Formats TextBlock(s) into usable HTML code"""
        formatted_block = text.TextFormatter(block, url_handler=self.url_handler).format()
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

    def format_unsupported(self, block):
        """Formats a placeholder for unsupported NPF types"""
        self.has_render_error = True

        with dominate.tags.div(cls="unsupported-content-block") as unsupported:
            with dominate.tags.div(cls="unsupported-content-block-message"):
                dominate.tags.h1("Unsupported content placeholder")
                dominate.tags.p(f"Hello! I'm a placeholder for the unsupported \"{block.type}\" type NPF content block."
                                f" Please report me!")

        return unsupported

    def _format_image(self, block, row_length=1):
        """Renders an ImageBlock into HTML"""
        figure = dominate.tags.figure(cls="image-block")
        figure.add(image.format_image(block, row_length, url_handler=self.url_handler))

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
            case objects.unsupported.Unsupported():
                return self.format_unsupported, (self.current,)
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
            blocks_in_layouts = []
            for layout in self.layout:
                if isinstance(layout, objects.layouts.Rows):
                    for row in layout.rows:
                        row_items = []
                        for index in row.ranges:
                            blocks_in_layouts.append(index)

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
                elif isinstance(layout, objects.layouts.AskLayout):
                    layout_items = []
                    for index in layout.ranges:
                        blocks_in_layouts.append(index)

                        render_instructions = self.render_instructions[index]
                        if not render_instructions:
                            continue

                        render_method, arguments = render_instructions
                        layout_items.append(render_method(*arguments))

                    self.post.add(
                        dominate.tags.div(
                            misc.format_ask(self.url_handler, *layout_items, blog_attribution=layout.attribution),
                            cls="layout-ask")
                    )

                else:
                    continue  # TODO: Unsupported layout type error

            # Edge case:
            # Sometimes only an "ask" layout is specified. In those circumstances the only thing we'll have added to our
            # HTML is the content blocks that makes up the ask. So we'll have some special handling here to handle
            # the leftovers that comes immediately after the ask.
            if len(self.layout) == 1 and isinstance(self.layout[0], objects.layouts.AskLayout):
                for index, render_instructions in enumerate(self.render_instructions):
                    if index in blocks_in_layouts:
                        continue
                    if not render_instructions:
                        continue

                    func, args = render_instructions
                    self.post.add(dominate.tags.div(func(*args), cls="layout-row"))

        else:
            for render_instructions in self.render_instructions:
                if not render_instructions:
                    continue

                func, args = render_instructions
                self.post.add(func(*args))

        if self.has_render_error:
            raise exceptions.RenderErrorDisclaimerError("Rendered post contains errors", rendered_result=self.post)

        return self.post


def format_content(parsed_contents, layouts=None, trails=None, url_handler=None):
    return Formatter(parsed_contents, layouts, url_handler=url_handler).format()
