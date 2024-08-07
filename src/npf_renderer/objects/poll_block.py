from collections import namedtuple
from typing import NamedTuple, Sequence, Optional, Dict


class PollResult(NamedTuple):
    is_winner: bool
    vote_count: int


class PollResults(NamedTuple):
    timestamp: int
    results: Dict[str, PollResult]


class PollBlock(NamedTuple):
    poll_id: str
    question: str

    # Mapping of answer id to answer
    # order is stored by the dictionary itself
    answers: dict

    creation_timestamp: int
    expires_after: int

    # TODO
    # source : str
    # multipleChoice : bool

    # Mapping of answer id to vote count
    votes: Optional[PollResults] = None

    # Aggregate count of votes for each answer
    total_votes: Optional[int] = None
