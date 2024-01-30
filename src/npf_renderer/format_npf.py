import dominate

from .format import Formatter
from .parse import Parser, LayoutParser
from . import exceptions


def format_npf(contents, layouts=None, *_, url_handler=None,
               forbid_external_iframes=False, pretty_html=False, poll_result_callback=None):
    """Formats the given NPF blocks into HTML
    
    Parameters:
        contents: Array of npf blocks to be parsed.
        layouts:  Layout information to arrange the NPF blocks into.
        url_handler:
            A function in which all URLs are passed into. Expects a string in return. 
            By default the internal logic will default to lambda url : url
        forbid_external_iframes: 
            When True embeds to external services won't be added 
            in the final output. This can change the resulting HTML of certain 
            blocks.
        pretty_html: Whether or not to render human readable html
        poll_result_callback:
            A function that accepts a `poll_id` parameter to request and return
            poll results. If unset, no poll results will be fetched.
    """
    contents = Parser(contents, poll_result_callback).parse()
    if layouts:
        layouts = LayoutParser(layouts).parse()

    try:
        contains_render_errors = False

        formatted = Formatter(
            contents,
            layouts, 
            url_handler=url_handler,
            forbid_external_iframes=forbid_external_iframes,
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
