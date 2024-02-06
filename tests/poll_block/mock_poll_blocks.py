import datetime

import dominate

from npf_renderer import objects


# Dominate does not support the time tag
class HTMLTimeTag(dominate.tags.html_tag):
    tagname="time"


basic_poll_data =  ({
    "type": "poll",
    "clientId": "0748f156-be02-4eaf-bbe4-5060d9992f93",
    "question": "This is a question",
    "answers": [
        {"clientId": "06a277ba-aeb4-4196-b585-2a1cdbbce849", "answerText": "answer 1"},
        {"clientId": "36885ab1-9e7f-4529-8408-b1477be0f93c", "answerText": "answer 2"},
        {"clientId": "698f4d74-069a-4d32-80a8-4a42e66fa36b", "answerText": "answer 3"},
        {"clientId": "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc", "answerText": "answer 4"},
    ]},

    # Basic object args
    ({
        "poll_id": "0748f156-be02-4eaf-bbe4-5060d9992f93",
        "question": "This is a question",
        "answers": {
            "06a277ba-aeb4-4196-b585-2a1cdbbce849": "answer 1",
            "36885ab1-9e7f-4529-8408-b1477be0f93c": "answer 2",
            "698f4d74-069a-4d32-80a8-4a42e66fa36b": "answer 3",
            "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": "answer 4",
        },
    }),

    # Results
    {
        "results": {
            "06a277ba-aeb4-4196-b585-2a1cdbbce849": 10,
            "36885ab1-9e7f-4529-8408-b1477be0f93c": 50,
            "698f4d74-069a-4d32-80a8-4a42e66fa36b": 500,
            "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": 250,
        },

        "timestamp": "1706611836"
    },

    dominate.tags.div(
        dominate.tags.div(
            dominate.tags.span(cls="vote-proportion", style="width: 1.235%;"),
            dominate.tags.span("answer 1", cls="answer"),
            dominate.tags.span(10, cls="vote-count"),
            cls="poll-choice"
        ),
        dominate.tags.div(
            dominate.tags.span(cls="vote-proportion", style="width: 6.173%;"),
            dominate.tags.span("answer 2", cls="answer"),
            dominate.tags.span(50, cls="vote-count"),
            cls="poll-choice"
        ),
        dominate.tags.div(
            dominate.tags.span(cls="vote-proportion", style="width: 61.728%;"),
            dominate.tags.span("answer 3", cls="answer"),
            dominate.tags.span(500, cls="vote-count"),
            cls="poll-choice poll-winner"
        ),
        dominate.tags.div(
            dominate.tags.span(cls="vote-proportion", style="width: 30.864%;"),
            dominate.tags.span("answer 4", cls="answer"),
            dominate.tags.span(250, cls="vote-count"),
            cls="poll-choice"
        ),
        cls="poll-body"
    )
)


simple_poll_expired = (
    {
        **basic_poll_data[0],
        "timestamp": 1672531220, "settings": {"expireAfter": "604800"}
    },

    objects.poll_block.PollBlock(**basic_poll_data[1], creation_timestamp=1672531220, expires_after=604800),

    dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        dominate.tags.div(
            dominate.tags.div(dominate.tags.span("answer 1", cls="answer"), cls="poll-choice"),
            dominate.tags.div(dominate.tags.span("answer 2", cls="answer"), cls="poll-choice"),
            dominate.tags.div(dominate.tags.span("answer 3", cls="answer"), cls="poll-choice"),
            dominate.tags.div(dominate.tags.span("answer 4", cls="answer"), cls="poll-choice"),
            cls="poll-body"
        ),
        dominate.tags.footer(
            dominate.tags.div(
                dominate.tags.span("Ended on: ", HTMLTimeTag("2023-01-08 00:00:20", datetime="2023-01-08T00:00")), 
                cls="poll-metadata"
            ),
        ),
        cls="poll-block expired-poll"
    ),

    dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        basic_poll_data[3],   # Answers
        dominate.tags.footer(

            dominate.tags.div(
                dominate.tags.span("810 votes"),
                dominate.tags.span("•", cls="separator"),
                dominate.tags.span("Ended on: ", HTMLTimeTag("2023-01-08 00:00:20", datetime="2023-01-08T00:00")),
                cls="poll-metadata"
            ),
        ),
        cls="poll-block expired-poll populated"
    ),
)


simple_ongoing_poll = (
    {
        **basic_poll_data[0],
        "timestamp": "1672531200", "settings": {"expireAfter": "604800"}
    },

    objects.poll_block.PollBlock(**basic_poll_data[1], creation_timestamp=1672531200, expires_after=604800),

    dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        dominate.tags.div(
            dominate.tags.div(dominate.tags.span("answer 1", cls="answer"), cls="poll-choice"),
            dominate.tags.div(dominate.tags.span("answer 2", cls="answer"), cls="poll-choice"),
            dominate.tags.div(dominate.tags.span("answer 3", cls="answer"), cls="poll-choice"),
            dominate.tags.div(dominate.tags.span("answer 4", cls="answer"), cls="poll-choice"),
            cls="poll-body"
        ),

        dominate.tags.footer(
            dominate.tags.div(
                dominate.tags.span("Remaining time: ", HTMLTimeTag("7 days, 0:00:00", datetime="P7D")),
                cls="poll-metadata"
            ),
        ),
        cls="poll-block"
    ),

    dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        basic_poll_data[3],   # Answers
        dominate.tags.footer(
            dominate.tags.div(
                dominate.tags.span("810 votes"),
                dominate.tags.span("•", cls="separator"),
                dominate.tags.span("Remaining time: ", HTMLTimeTag("7 days, 0:00:00", datetime="P7D")),
                cls="poll-metadata"
            ),
        ),
        cls="poll-block populated"
    ),
)


poll_with_extra_choice_without_any_results_attached = (
    {
        "type": basic_poll_data[0]["type"],
        "clientId": basic_poll_data[0]["clientId"],
        "question": basic_poll_data[0]["question"],
        "answers": ( 
            basic_poll_data[0]["answers"] +
            [{"clientId": "77795a6a-2ada-44ab-b8cc-b204c350c1be", "answerText": "answer 5"},]
        ),

        "timestamp": 1672531220, "settings": {"expireAfter": "604800"}
    },

    objects.poll_block.PollBlock(
        poll_id="0748f156-be02-4eaf-bbe4-5060d9992f93",
        question="This is a question",
        answers={
            "06a277ba-aeb4-4196-b585-2a1cdbbce849": "answer 1",
            "36885ab1-9e7f-4529-8408-b1477be0f93c": "answer 2",
            "698f4d74-069a-4d32-80a8-4a42e66fa36b": "answer 3",
            "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": "answer 4",
            "77795a6a-2ada-44ab-b8cc-b204c350c1be": "answer 5",
        },
        creation_timestamp=1672531220, expires_after=604800
    ),

    dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 1.235%;"),
                    dominate.tags.span("answer 1", cls="answer"),
                    dominate.tags.span(10, cls="vote-count"),
                    cls="poll-choice"
                ),
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 6.173%;"),
                    dominate.tags.span("answer 2", cls="answer"),
                    dominate.tags.span(50, cls="vote-count"),
                    cls="poll-choice"
                ),
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 61.728%;"),
                    dominate.tags.span("answer 3", cls="answer"),
                    dominate.tags.span(500, cls="vote-count"),
                    cls="poll-choice poll-winner"
                ),
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 30.864%;"),
                    dominate.tags.span("answer 4", cls="answer"),
                    dominate.tags.span(250, cls="vote-count"),
                    cls="poll-choice"
                ),

                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 0.0%;"),
                    dominate.tags.span("answer 5", cls="answer"),
                    dominate.tags.span(0, cls="vote-count"),
                    cls="poll-choice"
                ),
                cls="poll-body"
            ),
        dominate.tags.footer(
            dominate.tags.div(
                dominate.tags.span("810 votes"),
                dominate.tags.span("•", cls="separator"),
                dominate.tags.span("Ended on: ", HTMLTimeTag("2023-01-08 00:00:20", datetime="2023-01-08T00:00")),
                cls="poll-metadata"
            ),
        ),
        cls="poll-block expired-poll populated"
    ),
)


mock_tied_poll = (
    simple_poll_expired[0],

    objects.poll_block.PollBlock(
        poll_id="0748f156-be02-4eaf-bbe4-5060d9992f93",
        question="This is a question",
        answers={
            "06a277ba-aeb4-4196-b585-2a1cdbbce849": "answer 1",
            "36885ab1-9e7f-4529-8408-b1477be0f93c": "answer 2",
            "698f4d74-069a-4d32-80a8-4a42e66fa36b": "answer 3",
            "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": "answer 4",
        },

        votes=objects.poll_block.PollResults(
            results={
                "698f4d74-069a-4d32-80a8-4a42e66fa36b": objects.poll_block.PollResult(True, 500),
                "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": objects.poll_block.PollResult(True, 500),
                "36885ab1-9e7f-4529-8408-b1477be0f93c": objects.poll_block.PollResult(False, 50),
                "06a277ba-aeb4-4196-b585-2a1cdbbce849": objects.poll_block.PollResult(False, 10),
            },
            timestamp="1706611836",
        ),

        total_votes=1060,
        creation_timestamp=1672531220, expires_after=604800
    ),

    # Results
    {
        "results": {
            "06a277ba-aeb4-4196-b585-2a1cdbbce849": 10,
            "36885ab1-9e7f-4529-8408-b1477be0f93c": 50,
            "698f4d74-069a-4d32-80a8-4a42e66fa36b": 500,
            "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": 500,
        },

        "timestamp": "1706611836"
    },

    dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 0.943%;"),
                    dominate.tags.span("answer 1", cls="answer"),
                    dominate.tags.span(10, cls="vote-count"),
                    cls="poll-choice"
                ),
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 4.717%;"),
                    dominate.tags.span("answer 2", cls="answer"),
                    dominate.tags.span(50, cls="vote-count"),
                    cls="poll-choice"
                ),
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 47.17%;"),
                    dominate.tags.span("answer 3", cls="answer"),
                    dominate.tags.span(500, cls="vote-count"),
                    cls="poll-choice poll-winner"
                ),
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 47.17%;"),
                    dominate.tags.span("answer 4", cls="answer"),
                    dominate.tags.span(500, cls="vote-count"),
                    cls="poll-choice poll-winner"
                ),
                cls="poll-body"
            ),
        dominate.tags.footer(
            dominate.tags.div(
                dominate.tags.span("1060 votes"),
                dominate.tags.span("•", cls="separator"),
                dominate.tags.span("Ended on: ", HTMLTimeTag("2023-01-08 00:00:20", datetime="2023-01-08T00:00")),
                cls="poll-metadata"
            ),
        ),
        cls="poll-block expired-poll populated"
    ),
)


mock_multiple_winners_poll = (
    simple_poll_expired[0],

    objects.poll_block.PollBlock(
        poll_id="0748f156-be02-4eaf-bbe4-5060d9992f93",
        question="This is a question",
        answers={
            "06a277ba-aeb4-4196-b585-2a1cdbbce849": "answer 1",
            "36885ab1-9e7f-4529-8408-b1477be0f93c": "answer 2",
            "698f4d74-069a-4d32-80a8-4a42e66fa36b": "answer 3",
            "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": "answer 4",
        },

        votes=objects.poll_block.PollResults(
            results={
                "06a277ba-aeb4-4196-b585-2a1cdbbce849": objects.poll_block.PollResult(True,500),
                "36885ab1-9e7f-4529-8408-b1477be0f93c": objects.poll_block.PollResult(True,500),
                "698f4d74-069a-4d32-80a8-4a42e66fa36b": objects.poll_block.PollResult(True, 500),
                "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": objects.poll_block.PollResult(True, 500),
            },
            timestamp="1706611836",
        ),

        total_votes=2000,
        creation_timestamp=1672531220, expires_after=604800
    ),

    # Results
    {
        "results": {
            "06a277ba-aeb4-4196-b585-2a1cdbbce849": 500,
            "36885ab1-9e7f-4529-8408-b1477be0f93c": 500,
            "698f4d74-069a-4d32-80a8-4a42e66fa36b": 500,
            "2a1d4b7c-74aa-4be5-b2db-b9a017871bcc": 500,
        },

        "timestamp": "1706611836"
    },

    dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        dominate.tags.div(
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 25.0%;"),
                    dominate.tags.span("answer 1", cls="answer"),
                    dominate.tags.span(500, cls="vote-count"),
                    cls="poll-choice poll-winner"
                ),
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 25.0%;"),
                    dominate.tags.span("answer 2", cls="answer"),
                    dominate.tags.span(500, cls="vote-count"),
                    cls="poll-choice poll-winner"
                ),
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 25.0%;"),
                    dominate.tags.span("answer 3", cls="answer"),
                    dominate.tags.span(500, cls="vote-count"),
                    cls="poll-choice poll-winner"
                ),
                dominate.tags.div(
                    dominate.tags.span(cls="vote-proportion", style="width: 25.0%;"),
                    dominate.tags.span("answer 4", cls="answer"),
                    dominate.tags.span(500, cls="vote-count"),
                    cls="poll-choice poll-winner"
                ),
                cls="poll-body"
            ),
        dominate.tags.footer(
            dominate.tags.div(
                dominate.tags.span("2000 votes"),
                dominate.tags.span("•", cls="separator"),
                dominate.tags.span("Ended on: ", HTMLTimeTag("2023-01-08 00:00:20", datetime="2023-01-08T00:00")),
                cls="poll-metadata"
            ),
        ),
        cls="poll-block expired-poll populated"
    ),
)