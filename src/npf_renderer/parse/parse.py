"""Parses NPF Content blocks into python objects

parser = Parser(content_list)
results = parser.parse()

"""

import intervaltree

from . import misc, base
from .. import helpers, objects


class Parser(base.BaseParser):
    """All-in-one parser to process NPF content types"""

    def __init__(self, content, poll_result_callback=None):
        """Initializes the parser with a list of content blocks (json objects) to parse"""
        super().__init__(content)
        self.parsed_result = []
        self.poll_result_callback = poll_result_callback

    def _parse_text(self, nest_level=0, in_list_grouping=False):
        """Parses a NPF text content block into a TextBlock

        Takes the selected JSON text content block from `self.current` and parses it into a TextObject.
        Accepts a nest_level argument to handle any nesting.

        Args:
            nest_level: An argument representing how nested the current text block is in relations with other text
        blocks. In the original NPF this is represented as the indent_level. You should probably not be calling this
        method with that argument set as anything other than zero.

        Returns:
            'TextBlock' See documentation for that object for more information
        """

        def create_text_block(text_, subtype_, inline_formatting_, nest_=None):
            """Create a TextBlock object based on the data we have parsed"""
            if not nest_:
                nest_ = None

            return objects.text_block.TextBlock(
                text=text_,
                subtype=subtype_,
                nest=nest_,
                inline_formatting=inline_formatting_,
            )

        text = self.current["text"]
        if subtype := self.current.get("subtype"):
            subtype = getattr(objects.text_block.Subtypes, subtype.upper().replace("-", "_"))

        inline_formats = None
        if inline_formatting := self.current.get("formatting"):
            inline_formats = self._parse_inline_text(inline_formatting)

        # Begins the check to see if we have any children in the next element(s)
        nest_array = []
        while peek := self.peek():
            # Our children can only be TextBlock and ones with a set indent_level attr (which implies that they are
            # related to us)
            #
            # When an indent_level attr is set, we should also probably either be one of the list subtypes or a indented
            # block quote subtype. This check shouldn't be needed, however.
            indent_level = self.get_or("indent_level", "indentLevel", target=peek)

            if peek["type"] != "text" or indent_level is None:
                break

            # If the next element's indent level is higher than ours (stored as nest_level), they are our children.
            # Thus, we'll store them under us.
            if indent_level > nest_level:
                self.next()
                nested_block = self._parse_text(nest_level=nest_level + 1)
                nest_array.append(nested_block)

            else:
                # If not however, then they are either our siblings,  in the same level as our parent,
                # or an even "higher" (or lower with regard to indent_level) level. Therefore, there is nothing else
                # we need to do here
                break

        # Lists of the same type after to us should be merged into a ListGrouping, provided we aren't already in the
        # process of constructing one at our level.
        if not in_list_grouping and subtype in objects.text_block.ListsSubtype:
            list_grouping = [create_text_block(text, subtype, inline_formats, nest_=nest_array)]
            while peek := self.peek():
                if peek_subtype := peek.get("subtype"):
                    peek_subtype = getattr(objects.text_block.Subtypes, peek_subtype.upper().replace("-", "_"))

                # Make sure we are at the same nest level and that we are the same list type
                indent_level = self.get_or("indent_level", "indentLevel", target=peek) or 0

                if peek_subtype != subtype or indent_level != nest_level:
                    break

                self.next()

                list_grouping.append(self._parse_text(in_list_grouping=True, nest_level=nest_level))

            # If we're at the end then we don't have a peek() to compare to. Thus, we'll compare the
            # currently selected text block and the one that we have in the current context
            if list_grouping:
                return objects.text_block.ListGrouping(type=subtype, group=list_grouping)

        return create_text_block(text, subtype, inline_formats, nest_=nest_array)

    @staticmethod
    def route_inline_format(inline_format):
        inline_type = getattr(objects.inline.FMTTypes, inline_format["type"].upper())

        match inline_type:
            case (
                objects.inline.FMTTypes.BOLD
                | objects.inline.FMTTypes.ITALIC
                | objects.inline.FMTTypes.STRIKETHROUGH
                | objects.inline.FMTTypes.SMALL
            ):
                return objects.inline.Instruction(type_=inline_type)
            case objects.inline.FMTTypes.LINK:
                return objects.inline.LinkInstruction(type_=inline_type, url=inline_format["url"])
            case objects.inline.FMTTypes.MENTION:
                blog = inline_format["blog"]
                return objects.inline.MentionInstruction(
                    type_=inline_type, blog_name=blog["name"], blog_uuid=blog["uuid"], blog_url=blog["url"]
                )
            case objects.inline.FMTTypes.COLOR:
                return objects.inline.ColorInstruction(
                    type_=inline_type,
                    hex=inline_format["hex"],
                )

    def _parse_inline_text(self, raw_inline_formatting):
        """Parses the inline formatting of a content block into an array of inline fmt objects"""
        # The Interval Tree is needed to convert NPF inline fmt intervals
        # into discrete non-overlapping chunks.
        #
        # This is to simplify the final formatting operation.
        #
        # For instance:
        #
        # {'end': 1, 'start': 5, 'type': 'bold'} and {'end': 2, 'start': 7, 'type': 'italics'}
        #
        # Would be converted to something like:
        # [1, 2, [bold]], [2,5, [bold, italics]], [5,7, [italics]]
        #

        inline_format_intervals = intervaltree.IntervalTree()

        # Insert
        for raw_inline in raw_inline_formatting:
            start = raw_inline["start"]
            end = raw_inline["end"]

            inline_format_intervals[start:end] = self.route_inline_format(raw_inline)

        inline_format_intervals.split_overlaps()
        inline_format_intervals = sorted(inline_format_intervals.items())

        # Merge duplicates
        latch = None
        discrete_formatting_instructions = []
        for interval in inline_format_intervals:
            if latch:
                if latch[0] == interval.begin and latch[1] == interval.end:
                    latch[2].append(interval.data)  # Data being a formatting instruction
                else:
                    discrete_formatting_instructions.append(latch)
                    latch = [interval[0], interval[1], [interval[2]]]
            else:
                latch = [interval[0], interval[1], [interval[2]]]

        # Validates that everything got added
        if not discrete_formatting_instructions:
            discrete_formatting_instructions.append(latch)
        else:
            last_raw_style = inline_format_intervals[-1]
            last_processed_style = discrete_formatting_instructions[-1]

            if last_raw_style.begin != last_processed_style[0] and last_raw_style.end != last_processed_style[1]:
                discrete_formatting_instructions.append(latch)

        # Package
        inline_formats = [
            objects.inline.StyleInterval(interval[0], interval[1], sorted(interval[2]))
            for interval in discrete_formatting_instructions
        ]
        return inline_formats

    def _parse_image_block(self):
        """Parses a NPF Image Content Block into a ImageBlock NamedTuple"""
        media_list = self._parse_media_object(self.current["media"])
        assert media_list

        alt_text = self.get_or("alt_text", "altText")

        caption = self.current.get("caption")

        if color_block := self.current.get("colors"):
            colors = [color_hex for color_hex in color_block.values()]
        else:
            colors = None

        if attribution := self.current.get("attribution"):
            attribution = misc.parse_attribution(attribution)

        return objects.image.ImageBlock(
            media=media_list, alt_text=alt_text, caption=caption, colors=colors, attribution=attribution
        )

    def _parse_link_block(self):
        """Parses a NPF Link Content Block into a LinkBlock NamedTuple"""
        url = self.current["url"]

        # Optional
        title = self.current.get("title")
        description = self.current.get("description")
        author = self.current.get("author")

        site_name = self.get_or("siteName", "site_name")
        display_url = self.get_or("displayUrl", "display_url")

        poster_media_object = self._parse_media_object(self.current.get("poster"))

        return objects.link_block.LinkBlock(
            url=url,
            title=title,
            description=description,
            author=author,
            site_name=site_name,
            display_url=display_url,
            poster=poster_media_object,
        )

    def _fetch_audiovisual(self):
        url = self.current.get("url")
        provider = self.current.get("provider")
        media = self._parse_media_object(self.current.get("media"))

        embed_html = self.get_or("embedHtml", "embed_html")
        embed_url = self.get_or("embedUrl", "embed_url")
        embed_iframe = self.get_or("embedIframe", "embed_iframe")

        if embed_iframe:
            embed_iframe = objects.video_block.EmbedIframeObject(
                embed_iframe["url"],
                embed_iframe["width"],
                embed_iframe["height"],
            )

        poster_media_object = self._parse_media_object(self.current.get("poster"))

        if attribution := self.current.get("attribution"):
            attribution = misc.parse_attribution(attribution)

        return url, media, poster_media_object, provider, embed_html, embed_url, embed_iframe, attribution

    def _parse_video_block(self):
        (
            url,
            media,
            poster_media_object,
            provider,
            embed_html,
            embed_url,
            embed_iframe,
            attribution,
        ) = self._fetch_audiovisual()

        filmstrip = self._parse_media_object(self.current.get("filmstrip"))

        return objects.video_block.VideoBlock(
            url=url,
            provider=provider,
            media=media,
            embed_html=embed_html,
            embed_iframe=embed_iframe,
            embed_url=embed_url,
            poster=poster_media_object,
            attribution=attribution,
            filmstrip=filmstrip,
        )

    def _parse_audio_block(self):
        (
            url,
            media,
            poster_media_object,
            provider,
            embed_html,
            embed_url,
            _,
            attribution,
        ) = self._fetch_audiovisual()

        title = self.current.get("title")
        artist = self.current.get("artist")
        album = self.current.get("album")

        return objects.audio_block.AudioBlock(
            url=url,
            provider=provider,
            media=media,
            embed_html=embed_html,
            embed_url=embed_url,
            poster=poster_media_object,
            attribution=attribution,
            title=title,
            artist=artist,
            album=album,
        )

    def _parse_poll_block(self):
        """Parses a NPF Poll Block into a PollBlock NamedTuple

        Also fetches the poll results through self.poll_result_callback
        when it is defined.
        """
        poll_id = self.get_or("clientId", "client_id")
        if poll_id is None:
            raise ValueError("Invalid poll ID")

        question = self.current["question"]

        answers = {}
        for raw_ans in self.current["answers"]:
            answer_id = self.get_or("clientId", "client_id", target=raw_ans)
            answer_text = self.get_or("answerText", "answer_text", target=raw_ans)

            if answer_id is None or answer_text is None:
                raise ValueError("Invalid poll answer")

            answers[answer_id] = answer_text

        votes = None
        total_votes = None

        if self.poll_result_callback:
            callback_response = self.poll_result_callback(poll_id)

            # {answer_id: vote_count}
            raw_results = callback_response["results"].items()
            processed_results = sorted(raw_results, key=lambda item: -item[1])

            votes_dict = {}
            total_votes = 0

            winner_votes = processed_results[0][1]

            for index, results in enumerate(processed_results):
                vote_count = results[1]
                total_votes += vote_count

                votes_dict[results[0]] = objects.poll_block.PollResult(
                    is_winner=(winner_votes == vote_count), vote_count=vote_count
                )

            votes = objects.poll_block.PollResults(timestamp=callback_response["timestamp"], results=votes_dict)

        creation_timestamp = self.current["timestamp"]
        expires_after = self.current["settings"]["expireAfter"]

        return objects.poll_block.PollBlock(
            poll_id=poll_id,
            question=question,
            answers=answers,
            creation_timestamp=int(creation_timestamp),
            expires_after=int(expires_after),
            votes=votes,
            total_votes=total_votes,
        )

    def _parse_media_object(self, raw_media_object):
        """Parses a NPF media object"""
        if raw_media_object:
            if not isinstance(raw_media_object, list):
                raw_media_object_list = [raw_media_object]
            else:
                raw_media_object_list = raw_media_object

            media_objects = []
            for poster in raw_media_object_list:
                media_objects.append(misc.parse_media_block(poster))
        else:
            media_objects = None

        return media_objects

    def __parse_block(self):
        """Parses a content block and appends the result to self.parsed_result

        Works by routing specific content types to corresponding parse methods
        """

        match self.current["type"]:
            case "text":
                block = self._parse_text()
            case "image":
                block = self._parse_image_block()
            case "link":
                block = self._parse_link_block()
            case "audio":
                block = self._parse_audio_block()
            case "video":
                block = self._parse_video_block()
            case "poll":
                block = self._parse_poll_block()
            case _:
                block = objects.unsupported.Unsupported(self.current["type"])

        self.parsed_result.append(block)

    def parse(self):
        """Begins the parsing chain and returns the final list of parsed objects"""
        while self.next():
            self.__parse_block()

        return self.parsed_result
