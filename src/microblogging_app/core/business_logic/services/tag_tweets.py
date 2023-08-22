from core.models import Tweet
from django.db.models import QuerySet

from microblogging_app.utils import query_debugger


@query_debugger
def get_tweets_from_tag_id(tag_id: int, country_id: int) -> QuerySet:
    """Function accepts an id of tag, id of country and return a QuerySet object of tweets."""

    tweets = (
        Tweet.objects.filter(user__country_id=country_id, tags__id=tag_id)
        .prefetch_related("tags")
        .select_related("user")
    )

    return tweets
