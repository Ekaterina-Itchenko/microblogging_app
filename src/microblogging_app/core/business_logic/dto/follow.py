from dataclasses import dataclass

from django.db.models import QuerySet


@dataclass
class FollowersDTO:
    """Data transfer object for storing and transferring data to followers view."""

    user_fullname: str
    followers: QuerySet
    followers_num: int
    following_num: int


@dataclass
class FollowingDTO:
    """Data transfer object for storing and transferring data to following view."""

    user_fullname: str
    following: QuerySet
    followers_num: int
    following_num: int
