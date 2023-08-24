import logging
from typing import TYPE_CHECKING

from core.business_logic.errors import CountryNotEnteredError
from core.models import Tag
from django.db.models import Count

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.db.models import QuerySet

logger = logging.getLogger(__name__)


@query_debugger
def get_most_popular_tags(country_id: int) -> QuerySet:
    """
    Function accepts an User object and return a QuerySet object that contains
    10 most popular tags in a user's country.
    """

    if country_id:
        tags = (
            Tag.objects.filter(tweets__user__country_id=country_id)
            .annotate(num_tweets=Count("tweets"))
            .order_by("-num_tweets", "name")[:10]
        )
        return tags
    else:
        logger.info(msg="A country isn't entered.")
        raise CountryNotEnteredError
