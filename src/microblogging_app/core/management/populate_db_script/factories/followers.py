from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        RandomDistinctObjectFromListProvider,
        RandomObjectFromListProvider,
    )


class FollowersFactory:
    """Contains methods for generating values for FollowersDTO."""

    def __init__(
        self,
        random_from_user_provider: RandomObjectFromListProvider,
        random_to_user_provider: RandomDistinctObjectFromListProvider,
    ):
        self._random_from_user_provider = random_from_user_provider
        self._random_to_user_provider = random_to_user_provider

    def generate(self) -> object:
        """Generates random data for FollowersDTO"""

        from_user = self._random_from_user_provider()
        to_user = self._random_to_user_provider(value=from_user)
        following_model: AbstractBaseUser = get_user_model().following.through
        return following_model(from_user=from_user, to_user=to_user)
