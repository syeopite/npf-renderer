import datetime

import dominate

from npf_renderer import objects

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
        dominate.tags.footer(dominate.tags.p(str("Poll ended on 2023-01-08 00:00:20"))),
        cls="poll-block expired-poll"
    ),

    dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        basic_poll_data[3],   # Answers
        dominate.tags.footer(
            dominate.tags.p(str("Final result from 810 votes")),
            dominate.tags.p(str("Poll ended on 2023-01-08 00:00:20"),
        )),
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

        dominate.tags.footer(dominate.tags.p(str("Poll ends in 7 days, 0:00:00"))),
        cls="poll-block"
    ),

    dominate.tags.section(
        dominate.tags.header(dominate.tags.h3("This is a question")),
        basic_poll_data[3],   # Answers
        dominate.tags.footer(
            dominate.tags.p(str("810 votes")),
            dominate.tags.p(str("Poll ends in 7 days, 0:00:00"),
        )),
        cls="poll-block populated"
    ),

)