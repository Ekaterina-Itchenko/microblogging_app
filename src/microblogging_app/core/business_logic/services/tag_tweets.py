from typing import Iterable

from core.models import Tag, Tweet

from microblogging_app.utils import query_debugger


@query_debugger
def get_tweets_from_tag_id(tag_id: int, country_id: int) -> tuple[Iterable, Tag]:
    """Function accepts an id of tag, id of country and return a QuerySet object of tweets."""
    tag = Tag.objects.get(id=tag_id)
    tweets = Tweet.objects.filter(user__country_id=country_id, tags__id=tag_id).select_related("user")

    return tweets, tag
