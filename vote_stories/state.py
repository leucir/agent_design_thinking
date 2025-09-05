from typing import TypedDict, List


class VoteStoriesState(TypedDict):
    """State for vote stories analysis"""
    story: str
    score: int
    arguments: List[str]