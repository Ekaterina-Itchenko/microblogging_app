from __future__ import annotations

from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.dao import TweetDAO
from core.management.populate_db_script.data_access.dto import RepostDTO

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        RandomDistinctValueFromListProvider,
        RandomValueFromListProvider,
    )


class RepostFactory:
    """Contains methods for generating values for RepostDTO."""

    def __init__(
        self,
        random_user_provider: RandomDistinctValueFromListProvider,
        random_tweet_provider: RandomValueFromListProvider,
        tweet_dao: TweetDAO,
    ):
        self._random_user_provider = random_user_provider
        self._random_tweet_provider = random_tweet_provider
        self._tweet_dao = tweet_dao

    def generate(self) -> RepostDTO:
        """Generates random data for RepostDTO"""

        tweet_id = self._random_tweet_provider()
        tweet_user_id = self._tweet_dao.get_user_id_by_tweet_id(tweet_id=tweet_id)
        user_id = self._random_user_provider(value=tweet_user_id)
        return RepostDTO(user_id=user_id, tweet_id=tweet_id)
