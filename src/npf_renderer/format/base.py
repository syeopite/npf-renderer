import datetime
import urllib.parse

import dominate.tags
import dominate.util

from . import text, image, misc
from .. import objects, helpers, exceptions


def _calculate_amount_to_pad_from_nested(block, parent=True):
    if container := getattr(block, "nest", None):
        amount_to_pad = len(block.nest)
    elif container := getattr(block, "group", None):
        # See commit 2e8953d0081ffbe777579fab95a2b98c99d01177 as to why we subtract one
        amount_to_pad = (len(block.group) - 1)
    else:
        return 0

    for child_block in container:
        if getattr(child_block, "nest", None) or getattr(child_block, "group", None):
            amount_to_pad += _calculate_amount_to_pad_from_nested(child_block, parent=False)

    return amount_to_pad


# Dominate does not support the time tag
class HTMLTimeTag(dominate.tags.html_tag):
    tagname="time"


class Formatter(helpers.CursorIterator):
    def __init__(self, content, layout=None, *, url_handler=None, forbid_external_iframes=False):
        """Initializes the parser with a list of content blocks (json objects) to parse"""
        super().__init__(content)

        if not url_handler:
            def url_handler(url):
                return url

        self.layout = layout
        self.current_context_padding = 0
        self.render_instructions = []

        self.url_handler = url_handler
        self.forbid_external_iframes = forbid_external_iframes

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

    def _format_image(self, block, row_length=1, override_padding=None):
        """Renders an ImageBlock into HTML"""
        figure = dominate.tags.figure(cls="image-block")

        image_container = image.format_image(
            block,
            row_length,
            url_handler=self.url_handler,
            override_padding=override_padding,
        )

        figure.add(image_container)

        if block.caption:
            figure.add(dominate.tags.figcaption(block.caption, cls="image-caption"))

        return figure

    def _format_link(self, block):
        container = dominate.tags.div(cls="link-block")
        anchor_content_wrapper = dominate.tags.a(href=self.url_handler(block.url), cls="link-block-link")
        container.add(anchor_content_wrapper)

        if block.poster:
            poster_container = dominate.tags.div(cls="poster-container")
            anchor_content_wrapper.add(poster_container)

            srcset = ", ".join(image.create_srcset(block.poster, self.url_handler))

            poster_container.add(
                dominate.tags.img(
                    srcset=srcset,
                    alt=block.site_name or "Link block poster",
                    sizes="(max-width: 540px) 100vh, 540px",
                )
            )

            if block.title:
                poster_container.add(
                    dominate.tags.div(
                        dominate.tags.span(dominate.util.text(block.title)), cls="link-block-title poster-overlay-text"
                    )
                )
        elif block.title:
            anchor_content_wrapper.add(
                dominate.tags.div(
                    dominate.tags.span(dominate.util.text(block.title)), cls="link-block-title"
                )
            )

        link_block_description_container = dominate.tags.div(cls="link-block-description-container")
        anchor_content_wrapper.add(link_block_description_container)

        if block.description:
            link_block_description_container.add(
                dominate.tags.p(dominate.util.text(block.description), cls="link-block-description")
            )

        subtitles_div = dominate.tags.div(cls="link-block-subtitles")
        link_block_description_container.add(subtitles_div)

        subtitles = dominate.tags.span()
        subtitles_div.add(subtitles)

        if block.site_name:
            site_name = block.site_name
        else:
            site_name = urllib.parse.urlparse(block.url).hostname or block.url

        if site_name:
            subtitles.add(dominate.tags.span(dominate.util.text(site_name)))

            # When an author name exists in addition to the site name then we add it both to the subtitles
            # separated by a |
            if block.author:
                subtitles.add(dominate.tags.span(dominate.util.text("|"), cls="site-name-author-separator"))
                subtitles.add(dominate.tags.span(dominate.util.text(block.author)))
        else:
            subtitles.add(dominate.tags.span(dominate.util.text(block.author)))

        return container

    def _format_video(self, block):
        """Renders a parsed NPF video block into HTML

        If the video is an embed and external iframes are disabled, a link block linking
        to the video will be rendered instead.

        """
        root_video_block_attrs = {"cls": "video-block"}
        video_container_attrs = {"cls": "video-container"}

        video = None

        # We'll only render the native media player if media exists
        use_native_player_route = False
        if block.media:
            media_url = urllib.parse.urlparse(block.media[0].url)

            # And provider is either tumblr or the media_url is from Tumblr
            if block.provider == "tumblr" or media_url.hostname.endswith(".tumblr.com"):
                use_native_player_route = True
            # elif not self.forbid_external_iframes:
            #     use_native_player_route = True

        if use_native_player_route:
            # Sometimes the provider will be tumblr but the actual media URL isn't from tumblr
            if not media_url.hostname.endswith(".tumblr.com"):
                return self._audiovisual_link_block_fallback(
                    block,
                    title="Error: Cannot construct video player",
                    description="Please click me to watch on the original site"
                )

            additional_attrs = {}
            width, height = block.media[0].width, block.media[0].height

            media_url = media_url.geturl()

            if block.poster:
                additional_attrs["poster"] = self.url_handler(block.poster[0].url)

            video = dominate.tags.video(
                dominate.tags.source(
                    src=self.url_handler(media_url), type=block.media[0].type
                ),
                width=width,
                height=height,
                controls=True,
                **additional_attrs
            )
        if not video and not self.forbid_external_iframes:
            if block.embed_iframe:
                additional_attrs = {}
                width, height = block.embed_iframe.width, block.embed_iframe.height

                # YouTube should have an hardcoded height of 300px for some reason
                if block.provider == "youtube":
                    height = 300

                if block.provider:
                    additional_attrs["title"] = block.provider

                video = dominate.tags.iframe(
                    src=block.embed_iframe.url,
                    width=f"{width}",
                    height=f"{height}",
                    scrolling="no",
                    frameborder="0",
                    **additional_attrs
                )
            elif block.embed_html:
                video = dominate.util.raw(block.embed_html)

        # If we are unable to render a video based on any of the above
        # We'll try to render a link block instead
        if not video:
            if self.forbid_external_iframes and (block.embed_html or block.embed_url or block.embed_iframe):
                return self._audiovisual_link_block_fallback(
                    block,
                    "Embeds are disabled",
                    f"Please click me to watch on the original site"
                )
            else:
                return self._audiovisual_link_block_fallback(
                    block,
                    "Error: unable to render video block",
                    f"Please click me to watch on the original site"
                )

        video_block = dominate.tags.div(**root_video_block_attrs)
        video_container = dominate.tags.div(**video_container_attrs)
        video_container.add(video)
        video_block.add(video_container)

        return video_block

    def _format_audio(self, block):
        """Renders a parsed NPF audio block into HTML

        If the audio is an embed and external iframes are disabled, a link block linking
        to the audio will be rendered instead.
        """
        audio = None

        # TODO 
        # Logic for audio and video block is quite similar. Should be refactored.

        # We'll only render the native media player if media exists
        use_native_player_route = False
        if block.media:
            media_url = urllib.parse.urlparse(block.media[0].url)

            # And provider is either tumblr or the media_url is from Tumblr
            if block.provider == "tumblr" or media_url.hostname.endswith(".tumblr.com"):
                use_native_player_route = True
            # elif not self.forbid_external_iframes:
            #     use_native_player_route = True

        if use_native_player_route:
            # Sometimes the provider will be tumblr.com but the actual media URL isn't from tumblr
            if not media_url.hostname.endswith(".tumblr.com"):
                return self._audiovisual_link_block_fallback(
                    block,
                    title="Error: Cannot construct audio player",
                    description="Please click me to listen on the original site",
                    site_name=media_url.hostname
                )

            media_url = media_url.geturl()

            audio_container = dominate.tags.section(cls="ap-container")

            audio_block_heading = dominate.tags.header(cls="ab-heading")
            audio_block_metadata = dominate.tags.div(cls="ab-metadata")

            metadata_elements = []
            if block.title:
                metadata_elements.append(dominate.tags.h3(block.title, cls="ab-title"))
            if block.artist:
                metadata_elements.append(dominate.tags.h4(block.artist, cls="ab-artist"))
            if block.album:
                metadata_elements.append(dominate.tags.h4(block.album, cls="ab-album"))

            if metadata_elements:
                [audio_block_metadata.add(el) for el in metadata_elements]
                audio_block_heading.add(audio_block_metadata)

            if block.poster:
                audio_block_heading.add(
                    dominate.tags.img(
                        src=self.url_handler(block.poster[0].url),
                        srcset=", ".join(image.create_srcset(block.poster, self.url_handler)),
                        alt=block.title or "Audio block poster",
                        sizes="(max-width: 540px) 100vh, 540px",
                        cls="ab-poster"
                    )
                )

            if metadata_elements or block.poster:
                audio_container.add(audio_block_heading)

            audio_container.add(
                dominate.tags.audio(
                    dominate.tags.source(src=self.url_handler(media_url), type=block.media[0].type),
                    controls=True
                    )
                )

            audio = audio_container

        if not audio and not self.forbid_external_iframes:
            if block.embed_html:
                audio = dominate.util.raw(block.embed_html)
            elif block.embed_url:
                audio = dominate.tags.iframe(src=block.embed_url, scrolling="no", frameborder="0")

        # If we are unable to render an audio block based on any of the above
        # We'll try to render a link block instead
        if not audio:
            if self.forbid_external_iframes and (block.embed_html or block.embed_url):
                return self._audiovisual_link_block_fallback(
                    block,
                    "Embeds are disabled",
                    f"Please click me to listen on the original site"
                )
            else:
                return self._audiovisual_link_block_fallback(
                    block,
                    "Error: unable to render audio block",
                    f"Please click me to listen on the original site"
                )

        audio_block = dominate.tags.div(cls="audio-block")
        audio_block.add(audio)
        return audio_block

    def _format_poll(self, block):
        """Renders a parsed NPF poll block into HTML"""
        poll_block = dominate.tags.section(cls="poll-block")
        with poll_block:
            with dominate.tags.header():
                dominate.tags.h3(block.question)

        poll_body = dominate.tags.div(cls="poll-body")

        for answer_id, answer in block.answers.items():
            poll_choice = dominate.tags.div(cls="poll-choice")
            poll_answer = dominate.tags.span(answer, cls="answer")

            if block.votes:
                votes = block.votes.results.get(answer_id, [False, 0]) 

                if votes[0] is True:
                    poll_choice["class"] += " poll-winner"

                poll_vote_proportion_element = dominate.tags.span(cls="vote-proportion")
                if block.total_votes != 0:
                    poll_vote_proportion_element["style"] = f"width: {round((votes[1]/block.total_votes) * 100, 3)}%;"

                poll_vote_count = dominate.tags.span(votes[1], cls="vote-count")

                poll_choice.add(
                    poll_vote_proportion_element,
                    poll_answer,
                    poll_vote_count
                )
            else:
                poll_choice.add(poll_answer)

            poll_body.add(poll_choice)

        footer = dominate.tags.footer()
        with footer:
            creation = datetime.datetime.utcfromtimestamp(block.creation_timestamp)
            expiration = datetime.datetime.utcfromtimestamp(block.creation_timestamp + block.expires_after)
            now = datetime.datetime.utcnow()

            # If not expired we display how many days till expired
            with dominate.tags.div(cls="poll-metadata"):
                if block.votes:
                    dominate.tags.span(f"{block.total_votes} votes")
                    dominate.tags.span("•", cls="separator")
                if expiration > now:
                    # Build time duration string
                    remaining_time = expiration - now
                    duration_string = helpers.build_duration_string(remaining_time)
                    dominate.tags.span(f"Remaining time: ", HTMLTimeTag(str(remaining_time), datetime=duration_string))
                else:
                    formatted_expiration = expiration.strftime("%Y-%m-%dT%H:%M")
                    dominate.tags.span(f"Ended on: ", HTMLTimeTag(str(expiration), datetime=formatted_expiration))

        poll_block.add(poll_body, footer)

        if now > expiration:
            poll_block["class"] += " expired-poll"

        if block.votes:
            poll_block["class"] += " populated"

        return poll_block

    def _audiovisual_link_block_fallback(self, block, title : str, description : str, site_name : str = None):
        """Renders a link block from the given audio or video block
        
        Used as a fallback when the audio or video block cannot be 
        rendered successfully into HTML
        """

        # We attempt to find a valid URL in order to create a link block:
        if block.url:
            url = block.url
        elif block.media:
            url = block.media[0].url
        else:
            raise ValueError

        site_name = site_name or block.provider

        if url:
            return self._format_link(
                objects.link_block.LinkBlock(
                    url,
                    title=title,
                    description=description,
                    poster=block.poster,
                    site_name=site_name,
                    display_url=block.url
                )
            )
        else:
            raise RuntimeError("Unable to render")
    
    def __prepare_instruction_for_current_block(self):
        """Finds and returns the instruction (method) necessary to render a content block"""
        match self.current:
            case objects.text_block.TextBlock():
                if self.current.nest:
                    self.current_context_padding = _calculate_amount_to_pad_from_nested(self.current)
                return self._format_text, (self.current,)
            case objects.text_block.ListGrouping():
                self.current_context_padding = _calculate_amount_to_pad_from_nested(self.current)

                return self._format_list, (self.current,)
            case objects.image.ImageBlock():
                return self._format_image, (self.current,)
            case objects.link_block.LinkBlock():
                return self._format_link, (self.current,)
            case objects.audio_block.AudioBlock():
                return self._format_audio, (self.current,)
            case objects.video_block.VideoBlock():
                return self._format_video, (self.current,)
            case objects.poll_block.PollBlock():
                return self._format_poll, (self.current,)
            case objects.unsupported.Unsupported():
                return self.format_unsupported, (self.current,)
            case _:  # Unreachable
                raise ValueError("Unable to format unsupported block. This block should've been replaced with the \"Unsupported\" during the parsing stage. Something has gone wrong.")

    def _pad(self):
        [self.render_instructions.append(None) for _ in range(self.current_context_padding)]
        self.current_context_padding = 0

    def _arrange_layout_section(self, row):
        """Returns a list of rendered blocks that are within the given layout section"""
        row_items = []

        return row_items

    def format(self):
        """Renders the list of content blocks into HTML"""
        while self.next():
            instruction = self.__prepare_instruction_for_current_block()
            self.render_instructions.append(instruction)
            self._pad()

        if self.layout:
            # List to keep track of blocks that have been added to layouts
            # this is used to handle the edge case in which only certain blocks have specified layouts but not others.
            blocks_in_layouts = []

            for layout in self.layout:
                if isinstance(layout, objects.layouts.Rows):
                    for row in layout.rows:
                        blocks_in_layouts += row.ranges
                        row_items = []

                        # Arrange blocks into layouts.
                        # The process works in two phrases. 
                        # 
                        # The first phrase produces a list of rows, with each item (save for images) 
                        # in the row rendered in their final html form. 
                        # 
                        # Images in the row however will be stored as a tuple of the render instruction, 
                        # and the original dimensions of the image. 
                        # This is so the image with the smallest aspect ratio  can be used to arrange the rest of the images.
                        #
                        # The second phrase will then iterate through rows with images, select the smallest aspect ratio,
                        # and render each image block into their html forms according to the selected aspect ratio to use 
                        #
                        # TODO rephrase the above

                        has_image = False

                        for index in row.ranges:
                            render_instructions = self.render_instructions[index]
                            if not render_instructions:
                                continue

                            render_method, arguments = render_instructions

                            match render_method:
                                case self._format_image:
                                    has_image = True
                                    image_block = arguments[0]

                                    # TODO add tests for image blocks missing hasOriginalDimensions attr
                                    original_media = [media for media in image_block.media if media.has_original_dimensions]
                                    original_media = original_media[0] if original_media else image_block.media[0]

                                    row_items.append((
                                        arguments, original_media
                                    ))
                                case _:
                                    row_items.append(render_method(*arguments))

                        if not row_items:
                            continue
                    
                        if has_image:
                            original_media_ratios = []
                            images_in_row = []

                            for item_index, item in enumerate(row_items):
                                if not isinstance(item, tuple):
                                    continue

                                images_in_row.append((item_index, item[0])) 
                                original_media_ratios.append(round((item[1].height / item[1].width) * 100, 4))
                            
                            padding_ratio = min(original_media_ratios)
                            for index, render_instruction_args in images_in_row:
                                row_items[index] = self._format_image(*render_instruction_args, len(images_in_row), override_padding=padding_ratio)

                        row_tag = dominate.tags.div(cls="layout-row")
                        self.post.add(row_tag)

                        [row_tag.add(i) for i in row_items]
                elif isinstance(layout, objects.layouts.AskLayout):
                    layout_items = []
                    for index in layout.ranges:
                        blocks_in_layouts.append(index)

                        render_instruction = self.render_instructions[index]
                        if not render_instruction:
                            continue

                        render_method, args = render_instruction
                        layout_items.append(render_method(*args))

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
                for index, render_instruction in enumerate(self.render_instructions):
                    if (index in blocks_in_layouts) or (not render_instruction):
                        continue

                    render_method, args = render_instruction
                    self.post.add(dominate.tags.div(render_method(*args), cls="layout-row"))
        else:
            for render_instruction in self.render_instructions:
                if not render_instruction:
                    continue

                render_method, args = render_instruction
                self.post.add(render_method(*args))

        if self.has_render_error:
            raise exceptions.RenderErrorDisclaimerError("Rendered post contains errors", rendered_result=self.post)

        return self.post

