from dataclasses import dataclass

from core.models import Tag, Tweet
from django.db.models import QuerySet


@dataclass
class TweetTagsDTO:
    tweets: QuerySet[Tweet]
    tag: Tag
