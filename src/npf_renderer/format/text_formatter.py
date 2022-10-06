from dominate import tags
from dominate.util import text as raw_html_text

from src.npf_renderer.objects import text_block
from . import base


class FormatText(base.BaseFormatter):
    def __init__(self, parent_tag, content_block: text_block.TextBlock, layout=None, trails=None):
        self.parent_tag = parent_tag
        self.content = content_block

        self.child_section = self.__generate_child_post()
        # self.layout = layout
        # self.trails = trails

    def __generate_child_post(self):
        if subtype := self.content.subtype:
            match subtype:
                case text_block.Subtypes.HEADING1:
                    return tags.h1(cls="heading1")
                case text_block.Subtypes.HEADING2:
                    return tags.h2(cls="heading2")
                case text_block.Subtypes.QUIRKY:
                    return tags.p(cls="quirky")
                case text_block.Subtypes.QUOTE:
                    return tags.blockquote(cls="quote")
                case text_block.Subtypes.INDENTED:
                    return tags.blockquote(cls="indented")
                case text_block.Subtypes.CHAT:
                    return tags.p(cls="chat")

                # The list subtypes needs some special handling as 1. If they're the first in a specific level then
                # they'll create the list type 2. The text needs to be in a <li> element 3. They can be nested and
                # when nested we need to merge lists of the same level (except lvl 0) together. (We're assuming that
                # Tumblr's API won't be returning different lists in the same level)

                case text_block.Subtypes.ORDERED_LIST_ITEM:
                    return tags.ol(cls="ordered-list-item")
                case text_block.Subtypes.UNORDERED_LIST_ITEM:
                    return tags.ul(cls="unordered-list-item")

    # def __handle_list_subtypes(self, ordered):
    #     def create_list():
    #         """Quick helper function to create list elements"""
    #         if ordered:
    #             return tags.ol(cls="ordered-list-item")
    #         else:
    #             return tags.ul(cls="unordered-list-item")
    #         pass
    #
    #     # This makes it so that only children *tags* are shown
    #     # We start backwards so that we can get the list type closest to us
    #     list_of_parent_children_tags = [
    #         children for children in reversed(self.parent_tag.children) if isinstance(children, tags.dom_tag)
    #     ]
    #
    #     # Our parent has no children (yet. We'll become their children soon enough)
    #     if len(list_of_parent_children_tags) == 0:
    #         return create_list()
    #
    #     # These can be mixed: an ordered-list can be nested inside an unordered list and vice versa, and even in
    #     # indented blockquotes (but note that there can only be *one subtype* and it will be that of the *closest
    #     # tag*, so an ordered-list-item nested inside a blockquote will have indent_level 1 but be subtype
    #     # ordered-list-item).
    #     #
    #     # https://www.tumblr.com/docs/npf
    #
    #     if self.content.indent_level and self.content.indent_level > 0:
    #         children = list_of_parent_children_tags[0]
    #         # Break as soon as we see a list element to use
    #         if isinstance(children, (tags.ul, tags.ol)):
    #             return children  # Aka the list element we want to add to
    #
    #         # We haven't found a previously created list element, so we create one ourselves
    #         return create_list()
    #     else:
    #         # We are not currently nested in another element. So we quickly do a search:
    #         # If the previous tag is not one of a list, we'll create one.
    #         # If the previous tag is a list and is the same type as us we'll use that one
    #         # If the previous tag is a list but not of the same type as us, we won't use that and instead create our own
    #
    #         if len(list_of_parent_children_tags) == 0:
    #             return create_list()
    #         else:
    #             element = list_of_parent_children_tags[0]
    #             if ordered:
    #                 return element if isinstance(element, tags.ol) else tags.ol(cls="ordered-list-item")
    #             else:
    #                 return element if isinstance(element, tags.ul) else tags.ul(cls="unordered-list-item")

    def format(self):
        if not self.content.inline_formatting:
            if self.content.subtype in (text_block.Subtypes.ORDERED_LIST_ITEM, text_block.Subtypes.UNORDERED_LIST_ITEM):
                self.child_section.add(tags.li(self.content.text))
            else:
                self.child_section.add(raw_html_text(self.content.text))
        else:
            pass

        return self.child_section

# class __InlineFormatter:
#     def __init__(self, parent_post, content_block):
#         self.parent_post = parent_post
#         self.content_block = content_block
#
#         self.cursor = 0
#         self.curr_inline_rule_index = None
#         self.curr_inline_fmt_op = None
#         self.curr_letter = None
#
#     def __letter_generator(self):
#         pass
