simple_test = (  # Basic Example
    {
        "content": [
            {
                "type": "text",
                "text": "Hello world!"
            }
        ]
    },
    "b3d4c7a8e759763dddb06d05b2c86d5eb13f4b46"
)

longer_and_with_empty_string_test = (  # Empty Space Test
    {
        "content": [
            {
                "type": "text",
                "text": "ello!"
            },
            {
                "type": "text",
                "text": ""
            },
            {
                "type": "text",
                "text": "my name is cyle!"
            }
        ]
    },
    "a4fb1c72c9dbbd3abae5c29f39089547972058c6"
)

subtype_string_test = (
    {
        "content": [
            {
                "type": "text",
                "subtype": "heading1",
                "text": "New Post Forms Manifesto"
            },
            {
                "type": "text",
                "text": "There comes a moment in every company's life that they must redefine the rules..."
            },
            {
                "type": "text",
                "text": "We can choose to embrace this moment courageously, or we may choose to cower in fear."
            }
        ]
    },
    "a8f3095c2f57025a23ea2eb6b9eff9b6538e6f44"
)

subtype_string_test_2 = (
    {
        "content": [
            {
                "type": "text",
                "subtype": "heading1",
                "text": "Sward's Shopping List"
            },
            {
                "type": "text",
                "subtype": "ordered-list-item",
                "text": "Sword"
            },
            {
                "type": "text",
                "subtype": "ordered-list-item",
                "text": "Candy"
            },
            {
                "type": "text",
                "text": "But especially don't forget:"
            },
            {
                "type": "text",
                "subtype": "unordered-list-item",
                "text": "Death, which is uncountable on this list."
            }
        ]
    },

    "b3cadb14b69caca25da3d11bfd7ae84679611aeb"
)

subtype_and_indent_level_test = (
{
    "content": [
        {
            "type": "text",
            "subtype": "heading1",
            "text": "Sward's Shopping List"
        },
        {
            "type": "text",
            "subtype": "ordered-list-item",
            "text": "First level: Fruit",
        },
        {
            "type": "text",
            "subtype": "unordered-list-item",
            "text": "Second level: Apples",
            "indent_level": 1
        },
        {
            "type": "text",
            "subtype": "ordered-list-item",
            "text": "Third Level: Green",
            "indent_level": 2
        },
        {
            "type": "text",
            "subtype": "unordered-list-item",
            "text": "Second level: Pears",
            "indent_level": 1
        },
        {
            "type": "text",
            "subtype": "ordered-list-item",
            "text": "First level: Pears",
        }
    ]
}, "45387e623aa404082bab47155f758812f94d8234"
)

inline_formatting_test = (
    {"content": [
        {
            "type": "text",
            "text": "some small text",
            "formatting": [
                {
                    "start": 5,
                    "end": 10,
                    "type": "small"
                }
            ]
        },
    ]},
    "e8bbcbc6a3c95bf926fbf55f6853c58e9a8832b4"
)

#     {"content": }, "12345"

inline_formatting_link_test = (
    {"content": [{
        "type": "text",
        "text": "Found this link for you",
        "formatting": [
            {
                "start": 6,
                "end": 10,
                "type": "link",
                "url": "https://www.nasa.gov"
            }
        ]
    }]}, "bc4210f4cf0b574128b5fec47b9080066d98c939"
)
inline_formatting_mention_test = ({"content": [{
    "type": "text",
    "text": "Shout out to @david",
    "formatting": [
        {
            "start": 13,
            "end": 19,
            "type": "mention",
            "blog": {
                "uuid": "t:123456abcdf",
                "name": "david",
                "url": "https://davidslog.com/",
            }
        }
    ]
}]}, "f02d678c2124238e6f8bcc493b08776dce74d818")

inline_formatting_color_test = ({"content": [{
    "type": "text",
    "text": "Celebrate Pride Month",
    "formatting": [
        {
            "start": 10,
            "end": 15,
            "type": "color",
            "hex": "#ff492f"
        }
    ]
}]}, "332a28f36f2cc38e7ee5a60095d655d027377866")

test_inline_overlapping = ({
    "content": [
        {
            "type": "text",
            "text": "supercalifragilisticexpialidocious",
            "formatting": [
                {
                    "start": 0,
                    "end": 20,
                    "type": "bold"
                },
                {
                    "start": 9,
                    "end": 34,
                    "type": "italic"
                }
            ]
        }
    ]
}, "740d07f3d27809e503c363439062735f59861575")
