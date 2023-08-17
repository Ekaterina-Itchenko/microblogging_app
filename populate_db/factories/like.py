from __future__ import annotations

from typing import TYPE_CHECKING

from data_access.dao import TweetDAO
from data_access.dto import LikeDTO

if TYPE_CHECKING:
    from providers import (
        RandomDistinctValueFromListProvider,
        RandomValueFromListProvider,
    )


class LikeFactory:
    """Contains methods for generating values for LikeDTO."""

    def __init__(
        self,
        random_user_provider: RandomDistinctValueFromListProvider,
        random_tweet_provider: RandomValueFromListProvider,
        tweet_dao: TweetDAO,
    ):
        self._random_user_provider = random_user_provider
        self._random_tweet_provider = random_tweet_provider
        self._tweet_dao = tweet_dao

    def generate(self) -> LikeDTO:
        """Generates random data for LikeDTO"""

        tweet_id = self._random_tweet_provider()
        tweet_user_id = self._tweet_dao.get_user_id_by_tweet_id(tweet_id=tweet_id)
        user_id = self._random_user_provider(value=tweet_user_id)
        return LikeDTO(user_id=user_id, tweet_id=tweet_id)
