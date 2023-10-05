from dataclasses import dataclass
from typing import Optional

from django.contrib.auth.models import AbstractBaseUser


@dataclass
class AddTweetDTO:
    """Data transfer object for storing and transferring data from AddTweetForm."""

    content: str
    tags: str
    user: Optional[AbstractBaseUser] = None
    reply_to_id: Optional[int] = None


@dataclass
class EditTweetDTO:
    """Data transfer object for storing and transferring data from EditTweetFrom."""

    content: str
    tags: str
    tweet_id: Optional[int] = None
