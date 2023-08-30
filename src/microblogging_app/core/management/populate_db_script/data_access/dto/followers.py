from dataclasses import dataclass


@dataclass
class FollowersDTO:
    """DTO for storing and transferring generated data that will be written to the "followers" table."""

    from_user_id: int
    to_user_id: int
