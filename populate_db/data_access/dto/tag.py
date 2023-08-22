from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class TagDTO:
    """DTO for storing and transferring generated data that will be written to the "tags" table."""

    name: str
    created_at: object = datetime.now(tz=timezone.utc)
    updated_at: object = datetime.now(tz=timezone.utc)
