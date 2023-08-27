from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import TweetTagsDTO
from core.business_logic.errors import TagNotFound
from core.business_logic.services.trending_in_your_country import get_yesterday_time
from core.models import Tag, Tweet
from django.db.models import Count

if TYPE_CHECKING:
    from core.business_logic.dto import TagDTO
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


def get_tweets_by_tag_name_country_name(tag_name: str, country_name: str) -> QuerySet:
    """Function accepts an id of tag, id of country and return a QuerySet object of tweets."""

    datetime_yesterday_start, datetime_yesterday_end = get_yesterday_time()

    tweets = (
        Tweet.objects.filter(
            user__country__name=country_name,
            tags__name=tag_name,
            created_at__gt=datetime_yesterday_start,
            created_at__lt=datetime_yesterday_end,
        )
        .select_related("user", "reply_to", "reply_to__user")
        .annotate(
            num_reposts=Count("reposts", distinct=True),
            num_likes=Count("likes", distinct=True),
            num_replies=Count("tweets_replies", distinct=True),
        )
        .prefetch_related("like", "repost", "tags")
        .order_by("-created_at")
    )

    return tweets


def get_tweets_by_tag_name(data: TagDTO) -> TweetTagsDTO:
    """Function accepts TagDTO and return a TweetsQuerySet object of tweets."""

    try:
        tag = Tag.objects.get(name=data.tag)
        tweets = (
            Tweet.objects.filter(tags=tag)
            .select_related("user", "reply_to", "reply_to__user")
            .annotate(
                num_reposts=Count("reposts", distinct=True),
                num_likes=Count("likes", distinct=True),
                num_replies=Count("tweets_replies", distinct=True),
            )
            .prefetch_related("like", "repost", "tags")
            .order_by("-created_at")
        )
        tag_tweet_dto = TweetTagsDTO(tweets=tweets, tag=tag)
    except Tag.DoesNotExist:
        logger.error(msg="Tag does not exist", extra={"tag_name": data.tag})
        raise TagNotFound

    return tag_tweet_dto
