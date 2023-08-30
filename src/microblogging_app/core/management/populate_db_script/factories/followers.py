from __future__ import annotations

from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.dto import FollowersDTO

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        RandomDistinctValueFromListProvider,
        RandomValueFromListProvider,
    )


class FollowersFactory:
    """Contains methods for generating values for FollowersDTO."""

    def __init__(
        self,
        random_from_user_provider: RandomValueFromListProvider,
        random_to_user_provider: RandomDistinctValueFromListProvider,
    ):
        self._random_from_user_provider = random_from_user_provider
        self._random_to_user_provider = random_to_user_provider

    def generate(self) -> FollowersDTO:
        """Generates random data for FollowersDTO"""

        from_user = self._random_from_user_provider()
        to_user = self._random_to_user_provider(value=from_user)
        return FollowersDTO(from_user_id=from_user, to_user_id=to_user)
