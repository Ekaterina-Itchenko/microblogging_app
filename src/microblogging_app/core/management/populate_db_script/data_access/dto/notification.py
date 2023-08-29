from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class NotificationUserDTO:
    """DTO for storing and transferring generated data that will be written to the "notifications_user" table."""

    user_id: int
    notification_id: int


@dataclass
class NotificationDTO:
    """DTO for storing and transferring generated data that will be written to the "notifications" table."""

    message: str
    user: NotificationUserDTO
    notification_type_id: int
    created_at: object = datetime.now(tz=timezone.utc)
    updated_at: object = datetime.now(tz=timezone.utc)
