import dominate.tags

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


class Formatter(helpers.CursorIterator):
    def __init__(self, content, layout=None, *, url_handler=None, reserve_space_for_images=False,
                 forbid_external_iframes=False):
        """Initializes the parser with a list of content blocks (json objects) to parse"""
        super().__init__(content)

        if not url_handler:
            def url_handler(url):
                return url

        self.layout = layout
        self.current_context_padding = 0
        self.render_instructions = []

        self.url_handler = url_handler
        self.reserve_space_for_images = reserve_space_for_images
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
        # On Chromium based browsers, images within a row can sometimes become squished and not of equal widths.
        # As such we'll have to explicitly specify the amount of space the images should take up in the row
        if row_length > 1 and not self.reserve_space_for_images:
            figure = dominate.tags.figure(cls="image-block", style=f"width: {round(100/row_length, 2)}%")
        elif self.reserve_space_for_images:
            figure = dominate.tags.figure(cls="image-block reserved-space-img")
        else:
            figure = dominate.tags.figure(cls="image-block")

        image_container = image.format_image(
            block,
            row_length,
            url_handler=self.url_handler,
            override_padding=override_padding,
            reserve_space_for_images=self.reserve_space_for_images
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

        if block.site_name or block.author:
            subtitles_div = dominate.tags.div(cls="link-block-subtitles")
            link_block_description_container.add(subtitles_div)

            subtitles = dominate.tags.span()
            subtitles_div.add(subtitles)

            if block.site_name:
                subtitles.add(dominate.tags.span(dominate.util.text(block.site_name)))

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

        if block.media:
            additional_attrs = {}
            width, height = block.media[0].width, block.media[0].height

            # if self.reserve_space_for_images:
            #     root_video_block_attrs["cls"] += " reserved-space-img"
            #     video_container_attrs["style"] = f"padding-bottom: {round((height / width) * 100, 4)}%;"

            if block.poster:
                additional_attrs["poster"] = self.url_handler(block.poster[0].url)

            video = dominate.tags.video(
                dominate.tags.source(
                    src=self.url_handler(block.media[0].url), type=block.media[0].type
                ),
                width=width,
                height=height,
                preload="none",
                controls=True,
                **additional_attrs
            )
        elif not self.forbid_external_iframes:
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
        if video is None:
            # If a url exists
            if block.url:
                return self._format_link(
                    objects.link_block.LinkBlock(
                        block.url,
                        title=f"Embedded videos are not supported",
                        description=f"Please click me to visit \"{block.provider}\" to watch the video",
                        poster=block.poster,
                        site_name=block.provider,
                        display_url=block.url
                    )
                )

            raise RuntimeError("Unable to render video")

        video_block = dominate.tags.div(**root_video_block_attrs)
        video_container = dominate.tags.div(**video_container_attrs)
        video_container.add(video)
        video_block.add(video_container)

        # if self.reserve_space_for_images:
        #     root_video_block_attrs["cls"] += " reserved-space-img"
        #     video_container_attrs["style"] = f"padding-bottom: {round((height / 540) * 100, 4)}%;"

        return video_block

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
            case objects.video_block.VideoBlock():
                return self._format_video, (self.current,)
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

