import dominate.tags

from .. import objects


class TextFormatter:
    def __init__(self, parent_tag: dominate.tags.dom_tag, text_block: objects.text_block.TextBlock,
                 layout=None, trails=None, create_list_element=True):
        self.parent_tag = parent_tag
        self.text_block = text_block

        self.create_list_element = create_list_element

        self.tag = self.create_tag()

    def create_tag(self):
        if not self.text_block.subtype:
            return dominate.tags.p(cls="text")

        match self.text_block.subtype:
            case objects.text_block.Subtypes.HEADING1:
                return dominate.tags.h1(cls="heading1")
            case objects.text_block.Subtypes.HEADING2:
                return dominate.tags.h2(cls="heading2")
            case objects.text_block.Subtypes.QUIRKY:
                return dominate.tags.p(cls="quirky")
            case objects.text_block.Subtypes.QUOTE:
                return dominate.tags.blockquote(cls="quote")
            case objects.text_block.Subtypes.INDENTED:
                return dominate.tags.blockquote(cls="indented")
            case objects.text_block.Subtypes.CHAT:
                return dominate.tags.p(cls="chat")

            case _:
                if self.create_list_element:
                    if self.text_block.subtype == objects.text_block.Subtypes.ORDERED_LIST_ITEM:
                        return dominate.tags.ol(cls="ordered-list")
                    elif self.text_block.subtype == objects.text_block.Subtypes.UNORDERED_LIST_ITEM:
                        return dominate.tags.ul(cls="unordered-list")
                else:
                    if self.text_block.subtype == objects.text_block.Subtypes.ORDERED_LIST_ITEM:
                        return dominate.tags.li(cls="ordered-list-item")
                    elif self.text_block.subtype == objects.text_block.Subtypes.UNORDERED_LIST_ITEM:
                        return dominate.tags.li(cls="unordered-list-item")

    def parse(self):
        pass



