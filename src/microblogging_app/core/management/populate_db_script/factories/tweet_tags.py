from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import Tweet

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        RandomObjectFromListProvider,
    )


class TweetTagsFactory:
    """Contains methods for generating values for TweetTagsDTO."""

    def __init__(
        self, random_tweets_provider: RandomObjectFromListProvider, random_tags_provider: RandomObjectFromListProvider
    ):
        self._random_tweets_provider = random_tweets_provider
        self._random_tags_provider = random_tags_provider

    def generate(self) -> Tweet.tags.through:
        """Generates random data for TweetTagsDTO"""

        return Tweet.tags.through(tweet=self._random_tweets_provider(), tag=self._random_tags_provider())
