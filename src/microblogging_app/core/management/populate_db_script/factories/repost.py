from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import Repost

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        RandomDistinctObjectFromListProvider,
        RandomObjectFromListProvider,
    )


class RepostFactory:
    """Contains methods for generating values for RepostDTO."""

    def __init__(
        self,
        random_user_provider: RandomDistinctObjectFromListProvider,
        random_tweet_provider: RandomObjectFromListProvider,
    ):
        self._random_user_provider = random_user_provider
        self._random_tweet_provider = random_tweet_provider

    def generate(self) -> Repost:
        """Generates random data for RepostDTO"""

        tweet = self._random_tweet_provider()
        user_tweet = tweet.user
        user = self._random_user_provider(value=user_tweet)
        return Repost(user=user, tweet=tweet)
