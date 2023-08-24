from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.errors import TagNotFound
from core.models import Tag, Tweet

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from core.business_logic.dto import TagDTO
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


@query_debugger
def get_tweets_by_tag_id_country_id(tag_id: int, country_id: int) -> tuple[QuerySet, Tag]:
    """Function accepts an id of tag, id of country and return a QuerySet object of tweets."""

    try:
        tag = Tag.objects.get(id=tag_id)
        tweets = Tweet.objects.filter(user__country_id=country_id, tags__id=tag_id).select_related("user")

    except Tag.DoesNotExist:
        logger.error(msg="Tag does not exist", extra={"tag": tag_id})
        raise TagNotFound

    return tweets, tag


@query_debugger
def get_tweets_by_tag_id(data: TagDTO) -> tuple[QuerySet, Tag]:
    """Function accepts an id of tag and return a QuerySet object of tweets."""

    try:
        tag = Tag.objects.get(name=data.tag)
        tweets = Tweet.objects.filter(tags=tag).select_related("user").order_by("-created_at", "content")

    except Tag.DoesNotExist:
        logger.error(msg="Tag does not exist", extra={"tag_name": data.tag})
        raise TagNotFound

    return tweets, tag
