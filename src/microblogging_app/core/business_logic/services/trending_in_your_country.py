import logging
from datetime import datetime, time, timedelta, timezone

from core.business_logic.errors import CountryNotEnteredError
from core.models import Tag
from django.db.models import Count, QuerySet

from microblogging_app.utils import query_debugger

logger = logging.getLogger(__name__)


def get_yesterday_time() -> tuple[datetime, datetime]:
    """Gets the start and end times of yesterday."""

    yesterday = datetime.now(tz=timezone.utc) - timedelta(days=1)

    time_00 = time(0)
    time_23_59_59 = time(23, 59, 59)

    datetime_yesterday_start = datetime.combine(yesterday, time_00)
    datetime_yesterday_end = datetime.combine(yesterday, time_23_59_59)

    return datetime_yesterday_start, datetime_yesterday_end


@query_debugger
def get_most_popular_tags(country_name: int) -> QuerySet:
    """
    Function accepts an User object and return a QuerySet object that contains
    10 most popular tags in a user's country.
    """

    datetime_yesterday_start, datetime_yesterday_end = get_yesterday_time()

    if country_name:
        tags = (
            Tag.objects.filter(
                tweets__user__country__name=country_name,
                tweets__created_at__gt=datetime_yesterday_start,
                tweets__created_at__lt=datetime_yesterday_end,
            )
            .annotate(num_tweets=Count("tweets"))
            .order_by("-num_tweets", "name")[:10]
        )
        return tags
    else:
        logger.info(msg="A country isn't entered.")
        raise CountryNotEnteredError
