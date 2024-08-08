from typing import NamedTuple


class EmbedIframeObject(NamedTuple):
    url: str
    width: int = 540
    height: int = 405
