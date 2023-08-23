from dataclasses import dataclass


@dataclass
class TweetDTO:
    content: str
    tags: str
