from dominate import tags

from src.npf_renderer.objects import TextBlock

from .text_formatter import FormatText



#
# def render_content(content, layout=None, trails=None, parent_tag=None, nest_level=0):
#     """Renders HTML from the given NPF content, layout and trails objects."""
#     last_block_render_set = None  # {last_block, last_rendered_block}
#
#     if not parent_tag:
#         parent_tag = tags.div(cls="Post")
#
#     content_iter = iter(content)
#
#     with parent_tag:
#         for block in content_iter:
#             rendered_block = __render_block(block, content_iter, parent_tag=parent_tag)
#
#             # (If applicable) Merge nested text block children with the parent we got from the last iteration
#             if isinstance(block, TextBlock) and block.indent_level:
#
#                 # If the current TextBlock has an indent_level then the previous block must also be a TextBlock in order
#                 # to act as a parent
#                 assert isinstance(last_block_render_set[0], TextBlock)
#                 last_block_render_set[1].add(rendered_block)
#                 continue
#
#             # Add the last block to the parent and set current block as the last to prepare for the next iteration
#             if last_block_render_set:
#                 parent_tag.add(last_block_render_set[1])
#             last_block_render_set = (block, rendered_block)
#
#     # # We should have one remaining block we haven't added to the parent_tag yet
#     # parent_tag.add(last_block_render_set[1])
#
#     return parent_tag


class Formatter:
    def __init__(self, content, layout=None, trails=None):
        self.content = content
        self.layout = layout
        self.trails = trails

        # Index of the content array
        self.cursor = 0
        self.current = self.content[self.cursor]
        self.content_length = len(content)

        self.post = tags.div(cls="Post")

    @property
    def at_end(self):
        return self.content_length - 1 == self.cursor

    def next(self):
        self.cursor += 1
        self.current = self.content[self.cursor]
        return self.current

    def peek(self):
        if self.at_end:
            return False
        return self.content[self.cursor + 1]

    def prev(self):
        self.cursor -= 1
        self.current = self.content[self.cursor]
        return self.current

    def __render_block(self, parent_tag=None, nest_level=0):
        if not parent_tag:
            parent_tag = self.post

        if isinstance(self.current, TextBlock):
            formatter = FormatText(parent_tag, self.current)
            rendered_content = formatter.format()

            # Check to see if we have any children. If so process them under us
            while peekaboo := self.peek():
                # Our children can only be TextBlock and ones with a set indent_level attr
                if (not isinstance(peekaboo, TextBlock)) or not peekaboo.indent_level:
                    return rendered_content

                # If the next element's indent level is higher than ours, they are our children. Thus, we'll process
                # them under us.
                if peekaboo.indent_level > nest_level:
                    self.next()
                    rendered_content.add(self.__render_block(parent_tag=rendered_content, nest_level=nest_level + 1))
                else:
                    return rendered_content

        else:  # This shouldn't happen
            rendered_content = None

        return rendered_content

    def render_content(self):
        """Renders HTML from the given NPF content, layout and trails objects."""

        with self.post:
            while not self.at_end:
                self.post.add(self.__render_block())
                self.next()

            # Handle the last block:
            self.post.add(self.__render_block())

        return self.post


        #     for block in content_iter:
        #         rendered_block = __render_block(block, content_iter, parent_tag=parent_tag)
        #
        #         # (If applicable) Merge nested text block children with the parent we got from the last iteration
        #         if isinstance(block, TextBlock) and block.indent_level:
        #
        #             # If the current TextBlock has an indent_level then the previous block must also be a TextBlock in order
        #             # to act as a parent
        #             assert isinstance(last_block_render_set[0], TextBlock)
        #             last_block_render_set[1].add(rendered_block)
        #             continue
        #
        #         # Add the last block to the parent and set current block as the last to prepare for the next iteration
        #         if last_block_render_set:
        #             parent_tag.add(last_block_render_set[1])
        #         last_block_render_set = (block, rendered_block)
        #
        # # # We should have one remaining block we haven't added to the parent_tag yet
        # # parent_tag.add(last_block_render_set[1])
        #
        # return parent_tag
