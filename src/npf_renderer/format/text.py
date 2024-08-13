"""An HTML renderer for the TextBlock object

formatter = TextFormatter(text_block)
formatter.parse()

"""

from typing import Callable

import dominate.tags
import dominate.util

from . import inline
from .. import objects


class TextFormatter:
    """An HTML renderer for the TextBlock object"""

    def __init__(
        self, text_block: objects.text_block.TextBlock, url_handler: Callable, layout=None, create_list_element=True
    ):
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
        self.additional_classes = ""

        if self.text_block.inline_formatting:
            formatter = inline.InlineFormatter(self.text_block.text, self.text_block.inline_formatting, url_handler)
            self.text_tag = formatter.format()

            self.additional_classes += " inline-formatted-block"
        else:
            self.text_tag = dominate.util.text(self.text_block.text)

        self.tag = self.create_tag()

        self.url_handler = url_handler

    def create_tag(self):
        """Create an HTML tag to use as the base for the current TextBlock

        Primary based on the subtype. If nonexistent, then a standard paragraph element is used.

        All elements have the text-block class
        All subtypes have classes corresponding to their types.

        If the text block has inline formatting then an additional inline-formatted class is added
        """
        if not self.text_block.subtype:
            return dominate.tags.p(cls="text-block")

        match self.text_block.subtype:
            case objects.text_block.Subtypes.HEADING1:
                return dominate.tags.h1(cls="text-block heading1" + self.additional_classes)
            case objects.text_block.Subtypes.HEADING2:
                return dominate.tags.h2(cls="text-block heading2" + self.additional_classes)
            case objects.text_block.Subtypes.QUIRKY:
                return dominate.tags.p(cls="text-block quirky" + self.additional_classes)
            case objects.text_block.Subtypes.QUOTE:
                return dominate.tags.blockquote(cls="text-block quote" + self.additional_classes)
            case objects.text_block.Subtypes.INDENTED:
                return dominate.tags.blockquote(cls="text-block indented" + self.additional_classes)
            case objects.text_block.Subtypes.CHAT:
                return dominate.tags.p(cls="text-block chat" + self.additional_classes)
            case objects.text_block.Subtypes.ORDERED_LIST_ITEM:
                return dominate.tags.li(cls="text-block ordered-list-item" + self.additional_classes)
            case objects.text_block.Subtypes.UNORDERED_LIST_ITEM:
                return dominate.tags.li(cls="text-block unordered-list-item" + self.additional_classes)

    def format(self):

        # We have children that needs to be added to us, and we cannot just make the working tag the
        # text contents and add to that. (Can't add to raw text and even if there is an inline-formatting div it still
        # wouldn't be valid HTML in some cases) It needs to be directly added to self.tag. So:
        if self.text_block.nest:
            working_tag = self.tag
            working_tag.add(self.text_tag)
        else:
            working_tag = self.text_tag
            self.tag.add(working_tag)

        # Has nested elements. Also means our subtype is either indented or one of the list types
        if self.text_block.nest:
            for element in self.text_block.nest:
                if isinstance(element, objects.text_block.ListGrouping):
                    if element.type == objects.text_block.Subtypes.ORDERED_LIST_ITEM:
                        list_tag = dominate.tags.ol(cls="ordered-list")
                    else:
                        list_tag = dominate.tags.ul(cls="unordered-list")

                    for block in element.group:
                        list_tag.add(TextFormatter(block, url_handler=self.url_handler).format())

                    working_tag.add(list_tag)
                else:
                    working_tag.add(TextFormatter(element, url_handler=self.url_handler).format())

        return self.tag
