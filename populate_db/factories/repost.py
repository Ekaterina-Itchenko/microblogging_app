from __future__ import annotations

from typing import TYPE_CHECKING

from data_access.dto import RepostDTO

if TYPE_CHECKING:
    from providers import RandomValueFromListProvider


class RepostFactory:
    """Contains methods for generating values for RepostDTO."""

    def __init__(
        self, random_user_provider: RandomValueFromListProvider, random_tweet_provider: RandomValueFromListProvider
    ):
        self._random_user_provider = random_user_provider
        self._random_tweet_provider = random_tweet_provider

    def generate(self) -> RepostDTO:
        """Generates random data for RepostDTO"""

        return RepostDTO(user_id=self._random_user_provider(), tweet_id=self._random_tweet_provider())
