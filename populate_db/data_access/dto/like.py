from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class LikeDTO:
    """DTO for storing and transferring generated data that will be written to the "likes" table."""

    user_id: int
    tweet_id: int
    created_at: object = datetime.now(tz=timezone.utc)
    updated_at: object = datetime.now(tz=timezone.utc)
