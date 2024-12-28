"""This module provides the default localization strings for npf-renderer"""

from .. import helpers

DEFAULT_LOCALIZATION = {
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
    "poll_total_vote_amount_func": lambda votes : f"{votes} votes",
    "poll_remaining_time": "Remaining time: {duration}",
    "poll_ended_on": "Ended on: {ended_date}",
    "format_duration_func": lambda duration: str(duration),
    "format_datetime_func": lambda datetime: str(datetime),
}
