from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import Like

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        RandomDistinctObjectFromListProvider,
        RandomObjectFromListProvider,
    )


class LikeFactory:
    """Contains methods for generating values for LikeDTO."""

    def __init__(
        self,
        random_user_provider: RandomDistinctObjectFromListProvider,
        random_tweet_provider: RandomObjectFromListProvider,
    ):
        self._random_user_provider = random_user_provider
        self._random_tweet_provider = random_tweet_provider

    def generate(self) -> Like:
        """Generates random data for LikeDTO"""

        tweet = self._random_tweet_provider()
        tweet_user = tweet.user
        user = self._random_user_provider(value=tweet_user)
        return Like(user=user, tweet=tweet)
