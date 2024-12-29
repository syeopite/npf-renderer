import dominate.tags
import dominate.util


def generate_image_block_html(index, siblings):
    inner = (
        dominate.tags.div(
            dominate.tags.img(
                src=f"https://example.com/example-image-{index}.png",
                srcset=f"https://example.com/example-image-{index}.png 540w",
                cls="image",
                loading="lazy",
                sizes=f"(max-width: 540px) {round(100 / siblings)}vh, {round(540 / siblings)}px",
                alt="image",
            ),
            cls="image-container",
            style="padding-bottom: 75.0%;",
        ),
    )

    return dominate.tags.figure(inner, cls="image-block")


basic_string_modification = {
    "contents": ({"type": "video", "url": "https://example.com/somevideo.mp4"},),
    "localizer": {
        "error_video_link_block_fallback_heading": "Oops! Unable to produce a video renderer",
        "video_link_block_fallback_description": "Instead... have a link! Click me to watch on the original site",
    },
    "answer": (
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.a(
                    dominate.tags.div(
                        dominate.tags.span("Oops! Unable to produce a video renderer"), cls="link-block-title"
                    ),
                    dominate.tags.div(
                        dominate.tags.p(
                            "Instead... have a link! Click me to watch on the original site",
                            cls="link-block-description",
                        ),
                        dominate.tags.div(
                            dominate.tags.span(dominate.tags.span("example.com")), cls="link-block-subtitles"
                        ),
                        cls="link-block-description-container",
                    ),
                    href="https://example.com/somevideo.mp4",
                    cls="link-block-link",
                ),
                cls="link-block",
            ),
            cls="post-body",
        )
    ),
}


ask_i18n = {
    "contents": [
        {"type": "text", "text": "Hi there"},
        # Uses default width and height of 540 x 405
        {"type": "image", "media": [{"url": "https://example.com/example-image-1.png"}]},
        {"type": "image", "media": [{"url": "https://example.com/example-image-2.png"}]},
        {"type": "image", "media": [{"url": "https://example.com/example-image-3.png"}]},
        {"type": "image", "media": [{"url": "https://example.com/example-image-4.png"}]},
        {"type": "image", "media": [{"url": "https://example.com/example-image-5.png"}]},
    ],
    "localizer": {"asker_and_ask_verb": "asked by {name}:", "asker_with_no_attribution": "Unknown User"},
    "layouts": [
        {
            "type": "ask",
            "blocks": [0, 1, 2],
            "attribution": None,
        },
        {
            "type": "rows",
            "display": [
                {"blocks": [0]},
                {"blocks": [1]},
                {"blocks": [2]},
                {"blocks": [3]},
                {"blocks": [4, 5]},
            ],
        },
    ],
    "answer": (
        dominate.tags.div(
            # Ask
            dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.div(
                        dominate.tags.div(
                            dominate.tags.p(
                                "asked by ",
                                dominate.util.raw(
                                    dominate.tags.strong("Unknown User", cls="asker-name").render(pretty=False)
                                ),
                                ":",
                                cls="asker",
                            ),
                            cls="ask-header",
                        ),
                        dominate.tags.div(
                            dominate.tags.p("Hi there", cls="text-block"),
                            generate_image_block_html(1, 1),
                            generate_image_block_html(2, 1),
                            cls="ask-content",
                        ),
                        cls="ask-body",
                    ),
                    dominate.tags.img(
                        src="https://assets.tumblr.com/images/anonymous_avatar_96.gif",
                        loading="lazy",
                        cls="avatar asker-avatar image",
                    ),
                    cls="ask",
                ),
                cls="layout-ask",
            ),
            dominate.tags.div(generate_image_block_html(3, 1), cls="layout-row"),
            dominate.tags.div(generate_image_block_html(4, 2), generate_image_block_html(5, 2), cls="layout-row"),
            cls="post-body",
        )
    ),
}


# Example is arabic
def sample_plural_handler(number):

    mod_100 = number % 100

    if number == 0:
        return "Plural Form 0"
    elif number == 1:
        return "Plural Form 1"
    elif number == 2:
        return "Plural Form 2"
    elif mod_100 >= 3 and mod_100 <= 10:
        return "Plural Form 3"
    elif mod_100 >= 11:
        return "Plural Form 4"
    else:
        return "Plural Form 5"


class HTMLTimeTag(dominate.tags.html_tag):
    tagname = "time"


def generate_mock_poll_based_on_number(number, expected_plural_form, poll_footer=None, expired=False):
    if number == 0:
        poll_choice_proportion_attrs = {}
        poll_choice_proportion_winner_attrs = {}
        poll_choice_classes = "poll-choice poll-winner"
        poll_choice_winner_classes = "poll-choice poll-winner"
    else:
        poll_choice_proportion_attrs = {"style": "width: 0.0%;"}
        poll_choice_proportion_winner_attrs = {"style": "width: 100.0%;"}
        poll_choice_classes = "poll-choice"
        poll_choice_winner_classes = "poll-choice poll-winner"

    if not poll_footer:
        poll_footer = (
            dominate.tags.footer(
                dominate.tags.div(
                    dominate.tags.span(f"{number} (Plural Form {expected_plural_form})"),
                    dominate.tags.span("•", cls="separator"),
                    dominate.tags.span(
                        "Remaining time: ",
                        dominate.util.raw(HTMLTimeTag("7 days, 0:00:00", datetime="P7D").render(pretty=False)),
                    ),
                    cls="poll-metadata",
                ),
            ),
        )

    return dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        dominate.tags.div(
            dominate.tags.div(
                dominate.tags.span(cls="vote-proportion", **poll_choice_proportion_attrs),
                dominate.tags.span("answer 1", cls="answer"),
                dominate.tags.span(0, cls="vote-count"),
                cls=poll_choice_classes,
            ),
            dominate.tags.div(
                dominate.tags.span(cls="vote-proportion", **poll_choice_proportion_attrs),
                dominate.tags.span("answer 2", cls="answer"),
                dominate.tags.span(0, cls="vote-count"),
                cls=poll_choice_classes,
            ),
            dominate.tags.div(
                dominate.tags.span(cls="vote-proportion", **poll_choice_proportion_attrs),
                dominate.tags.span("answer 3", cls="answer"),
                dominate.tags.span(0, cls="vote-count"),
                cls=poll_choice_classes,
            ),
            dominate.tags.div(
                dominate.tags.span(cls="vote-proportion", **poll_choice_proportion_winner_attrs),
                dominate.tags.span("answer 4", cls="answer"),
                dominate.tags.span(number, cls="vote-count"),
                cls=poll_choice_winner_classes,
            ),
            cls="poll-body",
        ),
        poll_footer,
        cls="poll-block" + (" expired-poll" if expired else "") + " populated",
    )


def generate_results_for_poll(number):
    return {
        "results": {
            "06a277ba-aeb4-4196-b585-2a1cdbbce849": 0,
            "36885ab1-9e7f-4529-8408-b1477be0f93c": 0,
            "698f4d74-069a-4d32-80a8-4a42e66fa36b": 0,
            "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": number,
        },
        "timestamp": "1706611836",
    }


can_format_plurals = {
    "contents": (
        {
            "type": "poll",
            "clientId": "0748f156-be02-4eaf-bbe4-5060d9992f93",
            "question": "This is a question",
            "answers": [
                {"clientId": "06a277ba-aeb4-4196-b585-2a1cdbbce849", "answerText": "answer 1"},
                {"clientId": "36885ab1-9e7f-4529-8408-b1477be0f93c", "answerText": "answer 2"},
                {"clientId": "698f4d74-069a-4d32-80a8-4a42e66fa36b", "answerText": "answer 3"},
                {"clientId": "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc", "answerText": "answer 4"},
            ],
            "timestamp": 1672531200,
            "settings": {"expireAfter": "604800"},
        },
    ),
    "localizer": {
        "poll_total_vote_amount_func": lambda votes: f"{votes} ({sample_plural_handler(votes)})",
    },
}


can_format_duration = {
    "contents": can_format_plurals["contents"],
    "localizer": {
        "format_duration_func": lambda duration: f"Just {duration.days} days remaining!",
    },
    "poll_footer": dominate.tags.footer(
        dominate.tags.div(
            dominate.tags.span(f"250 votes"),
            dominate.tags.span("•", cls="separator"),
            dominate.tags.span(
                "Remaining time: ",
                dominate.util.raw(HTMLTimeTag("Just 7 days remaining!", datetime="P7D").render(pretty=False)),
            ),
            cls="poll-metadata",
        ),
    ),
}


can_format_datetime = {
    "contents": can_format_plurals["contents"],
    "localizer": {
        "format_datetime_func": lambda datetime: f"{datetime.strftime("Ended on %Y-%m-%d")}",
    },
    "poll_footer": dominate.tags.footer(
        dominate.tags.div(
            dominate.tags.span(f"250 votes"),
            dominate.tags.span("•", cls="separator"),
            dominate.tags.span(
                "Ended on: ",
                dominate.util.raw(HTMLTimeTag("Ended on 2023-01-08", datetime="2023-01-08T00:00").render(pretty=False)),
            ),
            cls="poll-metadata",
        ),
    ),
}
