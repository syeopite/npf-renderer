"""An HTML renderer for the TextBlock object

formatter = TextFormatter(text_block)
formatter.parse()

"""

from typing import Callable

import dominate.tags
import dominate.util

from .. import objects
from . import inline


class TextFormatter:
    """An HTML renderer for the TextBlock object"""
    def __init__(self, text_block: objects.text_block.TextBlock, url_handler: Callable,
                 layout=None, trails=None, create_list_element=True):
        """Renders a TextBlock object into HTML

        You should probably not be using this class directly!

        Parameters:
            text_block:
                The TextBlock object in question.
            url_handler:
                A callable in which all URLs processed (during inline-formatting) are sent into and retrieved.
                Allows for the caller to alter URLs in the final formatted HTML.
            create_list_element:
                Boolean denoting whether list elements should be enclosed in a <ul> or <ol> element.
                Boolean denoting whether list elements should be enclosed in a <ul> or <ol> element.
                Level zero list merging is delegated to the outer formatter but everything below is handled through
                recursion within the logic of self.format(). See code for more information

        """
        self.text_block = text_block
        self.create_list_element = create_list_element
        self.tag = self.create_tag()

        self.url_handler = url_handler

        if self.text_block.inline_formatting:
            formatter = inline.InlineFormatter(self.text_block.text, self.text_block.inline_formatting, url_handler)
            self.text_tag = formatter.format()
        else:
            self.text_tag = dominate.util.text(self.text_block.text)

    def create_tag(self):
        """Create an HTML tag to use as the base for the current TextBlock

        Primary based on the subtype. If nonexistent, then a standard paragraph element is used.

        All elements have the text-block class
        All subtypes have classes corresponding to their types.

        If the text block has inline formatting then an additional inline-formatted class is added
        """
        additional_classes = ""
        if self.text_block.inline_formatting:
            additional_classes += " inline-formatted-block"

        if not self.text_block.subtype:
            return dominate.tags.p(cls="text-block")

        match self.text_block.subtype:
            case objects.text_block.Subtypes.HEADING1:
                return dominate.tags.h1(cls="text-block heading1" + additional_classes)
            case objects.text_block.Subtypes.HEADING2:
                return dominate.tags.h2(cls="text-block heading2" + additional_classes)
            case objects.text_block.Subtypes.QUIRKY:
                return dominate.tags.p(cls="text-block quirky" + additional_classes)
            case objects.text_block.Subtypes.QUOTE:
                return dominate.tags.blockquote(cls="text-block quote" + additional_classes)
            case objects.text_block.Subtypes.INDENTED:
                return dominate.tags.blockquote(cls="text-block indented" + additional_classes)
            case objects.text_block.Subtypes.CHAT:
                return dominate.tags.p(cls="text-block chat" + additional_classes)

            case _:
                if self.create_list_element:
                    if self.text_block.subtype == objects.text_block.Subtypes.ORDERED_LIST_ITEM:
                        return dominate.tags.ol(cls="text-block ordered-list" + additional_classes)
                    elif self.text_block.subtype == objects.text_block.Subtypes.UNORDERED_LIST_ITEM:
                        return dominate.tags.ul(cls="text-block unordered-list" + additional_classes)
                else:
                    if self.text_block.subtype == objects.text_block.Subtypes.ORDERED_LIST_ITEM:
                        return dominate.tags.li(cls="ordered-list-item" + additional_classes)
                    elif self.text_block.subtype == objects.text_block.Subtypes.UNORDERED_LIST_ITEM:
                        return dominate.tags.li(cls="unordered-list-item" + additional_classes)

    def format(self):

        # If we created a list element we are going to now create a list item for our text
        if self.text_block.subtype in objects.text_block.ListsSubtype:
            if self.create_list_element:
                if self.text_block.subtype == objects.text_block.Subtypes.ORDERED_LIST_ITEM:
                    working_tag = dominate.tags.li(self.text_tag, cls="ordered-list-item")
                elif self.text_block.subtype == objects.text_block.Subtypes.UNORDERED_LIST_ITEM:
                    working_tag = dominate.tags.li(self.text_tag, cls="unordered-list-item")
                else:  # Unreachable
                    raise RuntimeError
            else:
                # If we did not create a list element but we still have children that needs to be added to us,
                # we can't just make the working tag the text contents and add to that. (Can't add to raw text and
                # even if there is an inline-formatting div it still wouldn't be right) It needs to be directly added
                # to self.tag's li. So:
                if self.text_block.nest:
                    working_tag = self.tag
                    working_tag.add(self.text_tag)
                else:
                    working_tag = self.text_tag
        else:
            working_tag = self.text_tag

        if working_tag is not self.tag:
            self.tag.add(working_tag)

        # Has nested elements. Also means our subtype is either indented or one of the list types
        if self.text_block.nest:
            list_to_use = None
            first_time_trigger = True

            # These can be mixed... but note that **there can only be one subtype and it will be that of the closest
            # tag***...
            #
            # https://www.tumblr.com/docs/npf#text-block-subtype-list-item
            for element in self.text_block.nest:
                if element.subtype in objects.text_block.ListsSubtype:
                    if first_time_trigger:
                        first_time_trigger = False
                        list_to_use = TextFormatter(
                            element,
                            url_handler=self.url_handler
                        ).format()
                    else:
                        # If here then we've already created a list tag as the first_time_trigger option went off
                        # So subsequent list items at the same level are just going to use that one. We don't need to
                        # check if the list types are different because nested lists at the same level can only
                        # have the same type
                        list_item_tag = TextFormatter(
                            element,
                            create_list_element=False,
                            url_handler=self.url_handler
                        ).format()

                        list_to_use.add(list_item_tag)
                else:
                    working_tag.add(TextFormatter(element).format())

            working_tag.add(list_to_use)

        return self.tag
