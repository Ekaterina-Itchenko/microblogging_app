from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import Tweet

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        RandomObjectFromListOrNoneProvider,
        RandomObjectFromListProvider,
        RandomTextProvider,
    )


class TweetFactory:
    """Contains methods for generating values for TweetDTO."""

    def __init__(
        self,
        random_user_id_provider: RandomObjectFromListProvider,
        random_text_provider: RandomTextProvider,
        random_reply_to_provider: RandomObjectFromListOrNoneProvider,
    ):
        self._random_user_id_provider = random_user_id_provider
        self._random_reply_to_provider = random_reply_to_provider
        self._random_text_provider = random_text_provider

    def generate(self) -> Tweet:
        """Generates random data for TweetDTO"""

        return Tweet(
            user=self._random_user_id_provider(),
            content=self._random_text_provider(),
            reply_to=self._random_reply_to_provider(),
        )
