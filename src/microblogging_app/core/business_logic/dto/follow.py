from dataclasses import dataclass

from django.db.models import QuerySet


@dataclass
class FollowersDTO:
    """Data transfer object for storing and transferring data about followers."""

    user_fullname: str
    followers: QuerySet
    followers_num: int
    following_num: int


@dataclass
class FollowingDTO:
    """Data transfer object for storing and transferring data about following users."""

    user_fullname: str
    following: QuerySet
    followers_num: int
    following_num: int


@dataclass
class FollowersPageDTO:
    """Data transfer object for storing and transferring data to followers view."""

    user_fullname: str
    followers: QuerySet
    followers_num: int
    following_num: int
    user_username: str
    auth_user_following: QuerySet


@dataclass
class FollowingPageDTO:
    """Data transfer object for storing and transferring data to followers view."""

    user_fullname: str
    following: QuerySet
    followers_num: int
    following_num: int
    user_username: str
    auth_user_following: QuerySet
