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
    "be148356a4f66e8c7a11c829e476163ea3fa3dac"
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

    "c2282f20aadb75280632e31db95c7eaae5add2fd"
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
}, "b9c9d13c517d1eca77b64ef3b534ec06abad9a16"
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
    "bb53ffa588f8e48670959d60ef1e98a256c8b794"
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
    }]}, "163b2ebc5872199029d8f670e7a26a2149375656"
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
}]}, "c94e0d1d1009f7f3376486abe0b3bf811f649b9a")

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
}]}, "0812b6954481f0e76211693ef3733f590e766f64")

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
}, "6e81372ba5756d8d1cd77716e47917ca50af65f8")
