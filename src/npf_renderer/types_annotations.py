from . import objects

NPFBlocks = (
    objects.text_block.TextBlock
    | objects.image.ImageBlock
    | objects.link_block.LinkBlock
    | objects.video_block.VideoBlock
    | objects.audio_block.AudioBlock
    | objects.poll_block.PollBlock
)

JSONType = dict[str, "JSONType"] | list["JSONType"] | str | int | float | bool | None
