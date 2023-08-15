from __future__ import annotations

from typing import TYPE_CHECKING

from data_access.dto import LikeDTO

if TYPE_CHECKING:
    from providers import RandomValueFromListProvider


class LikeFactory:
    """Contains methods for generating values for LikeDTO."""

    def __init__(
        self, random_user_provider: RandomValueFromListProvider, random_tweet_provider: RandomValueFromListProvider
    ):
        self._random_user_provider = random_user_provider
        self._random_tweet_provider = random_tweet_provider

    def generate(self) -> LikeDTO:
        """Generates random data for LikeDTO"""

        return LikeDTO(user_id=self._random_user_provider(), tweet_id=self._random_tweet_provider())
