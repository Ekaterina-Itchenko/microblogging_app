from __future__ import annotations

from typing import TYPE_CHECKING

from data_access.dto import TweetDTO

if TYPE_CHECKING:
    from providers import (
        RandomTextProvider,
        RandomValueFromListOrNoneProvider,
        RandomValueFromListProvider,
    )


class TweetFactory:
    """Contains methods for generating values for TweetDTO."""

    def __init__(
        self,
        random_user_id_provider: RandomValueFromListProvider,
        random_text_provider: RandomTextProvider,
        random_reply_to_provider: RandomValueFromListOrNoneProvider,
    ):
        self._random_user_id_provider = random_user_id_provider
        self._random_reply_to_provider = random_reply_to_provider
        self._random_text_provider = random_text_provider

    def generate(self) -> TweetDTO:
        """Generates random data for TweetDTO"""

        return TweetDTO(
            user_id=self._random_user_id_provider(),
            content=self._random_text_provider(),
            reply_to=self._random_reply_to_provider(),
        )
