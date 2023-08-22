from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class TweetDTO:
    """DTO for storing and transferring generated data that will be written to the "tweets" table."""

    user_id: int
    content: str
    reply_to: int | None
    reply_counter: int = 0
    created_at: object = datetime.now(tz=timezone.utc)
    updated_at: object = datetime.now(tz=timezone.utc)
