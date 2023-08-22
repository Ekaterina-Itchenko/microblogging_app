from dataclasses import dataclass


@dataclass
class TweetTagsDTO:
    """DTO for storing and transferring generated data that will be written to the "tweet_tags" table."""

    tweet_id: int
    tag_id: int
