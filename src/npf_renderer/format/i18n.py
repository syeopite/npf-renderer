"""This module provides the default localization strings for npf-renderer"""


class MissingTranslationKey(Exception):
    pass


# Default localization strings used in npf-renderer
# Split into two categories. Strings, which  contain the strings and their plural for translations
# and formats which concern formatting various numbers and datetimes.
DEFAULT_LOCALIZATION = {
    "strings": {
        "asker_with_no_attribution": "Anonymous",
        "asker_and_ask_verb": "{name} asked:",
        "unsupported_block_header": "Unsupported NPF block",
        "unsupported_block_description": 'Placeholder for the unsupported "{block}" type NPF block\
    Please report me over at https://github.com/syeopite/npf-renderer',
        "generic_image_alt_text": "image",
        "link_block_poster_alt_text": 'Preview image for "{site}"',
        "link_block_fallback_embeds_are_disabled": "Embeds are disabled",
        "error_video_link_block_fallback_heading": "Error: unable to render video block",
        "video_link_block_fallback_description": "Please click me to watch on the original site",
        "error_link_block_fallback_native_video_player_non_tumblr_source": "Error: non-tumblr source for video player",
        "fallback_audio_block_thumbnail_alt_text": "Album art",
        "error_audio_link_block_fallback_heading": "Error: unable to render audio block",
        "audio_link_block_fallback_description": "Please click me to listen on the original site",
        "error_link_block_fallback_native_audio_player_non_tumblr_source": "Error: non-tumblr source for audio player",
        "plural_poll_total_votes": lambda votes: f"{votes} votes",
        "poll_remaining_time": "Remaining time: {duration}",
        "poll_ended_on": "Ended on: {ended_date}",
        "post_attribution": "From {author}",
        "blog_attribution": "Created by {author}",
        "app_attribution": "View on {platform}",
        "unsupported_attribution": 'Attributed via an unsupported ("{attributee}") attribution type. Please report this over at https://github.com/syeopite/npf-renderer',
        "format_duration_func": lambda duration: str(duration),
        "format_datetime_func": lambda datetime: str(datetime),
    },
    "formats": {
        "duration": {
            "__default__": lambda duration: str(duration),
            # "poll_duration": lambda duration: str(duration)
        },
        "datetime": {
            "__default__": lambda datetime: str(datetime)
            # "poll_ended_on": lambda duration: str(duration)
        },
    },
}


# Retrieves and formats the translation for the given key
def translate(localizer, key, *, number=None, **substitution):
    try:
        translated = localizer["strings"][key]

        if number is not None:
            translated = translated(number)

        if substitution:
            translated = translated.format(**substitution)

        return translated
    except KeyError:
        raise MissingTranslationKey()


# Retrieves and formats a datetime with the given key. Fallbacks to __default__ key if the given key cannot be found
def format_datetime(localizer, key, *args, **kwargs):
    try:
        formats_localizer = localizer["formats"]["datetime"]
        if (format_func := formats_localizer.get(key, None)) and format_func is not None:
            return format_func(*args, **kwargs)
        else:
            return formats_localizer["__default__"](*args, **kwargs)
    except KeyError:
        raise MissingTranslationKey()


# Retrieves and formats a duration with the given key. Fallbacks to __default__ key if the given key cannot be found
def format_duration(localizer, key, *args, **kwargs):
    try:
        formats_localizer = localizer["formats"]["duration"]
        if (format_func := formats_localizer.get(key, None)) and format_func is not None:
            return format_func(*args, **kwargs)
        else:
            return formats_localizer["__default__"](*args, **kwargs)
    except KeyError:
        raise MissingTranslationKey()
