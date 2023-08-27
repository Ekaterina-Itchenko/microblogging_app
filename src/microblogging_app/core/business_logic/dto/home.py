from dataclasses import dataclass

from core.models import Tweet
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import QuerySet


@dataclass
class FollowingTweetsRepostsDTO:
    """Data transfer object for storing and transferring data about following users' tweets and reposts."""

    tweets: QuerySet[Tweet]
    following_users: QuerySet[AbstractBaseUser]
