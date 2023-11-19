import dominate

from .format import Formatter
from .parse import Parser, LayoutParser
from . import exceptions


def format_npf(contents, layouts=None, *_, url_handler=None, skip_cropped_images=False, pretty_html=False):
    """Formats the given NPF blocks into HTML
    
    Parameters:
        contents: Array of npf blocks to be parsed.
        layouts:  Layout information to arrange the NPF blocks into.

        url_handler:
            A function in which all URLs are passed into. Expects a string in return. 
            By default the internal logic will default to lambda url : url

        skip_cropped_images: 
            Whether or not to include cropped images within the HTML output of this function. 
            By default every image within NPF's media blocks are used via the <img>'s srcset attribute
        
        pretty_html: Whether or not to render human readable html 
    """
    contents = Parser(contents).parse()
    if layouts:
        layouts = LayoutParser(layouts).parse()

    try:
        contains_render_errors = False

        formatted = Formatter(
            contents,
            layouts, 
            url_handler=url_handler,
            skip_cropped_images=skip_cropped_images
        ).format()

    except exceptions.RenderErrorDisclaimerError as e:
        contains_render_errors = True
        formatted = e.rendered_result
        assert formatted is not None
    except Exception as e:
        # TODO
        # Something had gone wrong block
        formatted = dominate.tags.div(cls="post-body")
        contains_render_errors = True

    return contains_render_errors, formatted.render(pretty=pretty_html)
