from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class RepostDTO:
    """DTO for storing and transferring generated data that will be written to the "reposts" table."""

    user_id: int
    tweet_id: int
    created_at: object = datetime.now(tz=timezone.utc)
    updated_at: object = datetime.now(tz=timezone.utc)
