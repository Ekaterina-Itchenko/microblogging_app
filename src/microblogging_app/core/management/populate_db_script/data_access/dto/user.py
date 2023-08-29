from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class UserDTO:
    """DTO for storing and transferring generated data that will be written to the "users" table."""

    description: str
    birth_date: str
    country_id: int
    username: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    unencrypted_password: str
    encrypted_password: str
    created_at: object = datetime.now(tz=timezone.utc)
    updated_at: object = datetime.now(tz=timezone.utc)
    is_superuser: bool = False
    is_staff: bool = False
