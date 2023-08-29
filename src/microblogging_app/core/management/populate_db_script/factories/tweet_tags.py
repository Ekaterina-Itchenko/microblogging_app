from __future__ import annotations

from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.dto import TweetTagsDTO

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import RandomValueFromListProvider


class TweetTagsFactory:
    """Contains methods for generating values for TweetTagsDTO."""

    def __init__(
        self, random_tweets_provider: RandomValueFromListProvider, random_tags_provider: RandomValueFromListProvider
    ):
        self._random_tweets_provider = random_tweets_provider
        self._random_tags_provider = random_tags_provider

    def generate(self) -> TweetTagsDTO:
        """Generates random data for TweetTagsDTO"""

        return TweetTagsDTO(tweet_id=self._random_tweets_provider(), tag_id=self._random_tags_provider())
