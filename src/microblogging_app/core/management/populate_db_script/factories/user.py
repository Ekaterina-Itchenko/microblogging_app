from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        PasswordProvider,
        RandomBirthDateProvider,
        RandomObjectFromListProvider,
        RandomTextProvider,
        RandomUserProfileProvider,
    )


class UserFactory:
    """Contains methods for generating values for UserDTO."""

    def __init__(
        self,
        random_country_provider: RandomObjectFromListProvider,
        random_text_provider: RandomTextProvider,
        random_birth_date_provider: RandomBirthDateProvider,
        random_profile_provider: RandomUserProfileProvider,
        password_provider: PasswordProvider,
    ):
        self._random_country_provider = random_country_provider
        self._random_text_provider = random_text_provider
        self._random_birth_date_provider = random_birth_date_provider
        self._random_profile_provider = random_profile_provider
        self._password_provider = password_provider

    def generate(self) -> AbstractBaseUser:
        """Generates random data for UserDTO"""
        user_model = get_user_model()
        profile = self._random_profile_provider()
        password = self._password_provider()
        description = self._random_text_provider()
        country = self._random_country_provider()
        birth_date = self._random_birth_date_provider()
        return user_model(
            description=description,
            country=country,
            birth_date=birth_date,
            username=profile["username"],
            first_name=profile["first_name"],
            last_name=profile["last_name"],
            email=profile["email"],
            is_active=True,
            password=password,
        )
