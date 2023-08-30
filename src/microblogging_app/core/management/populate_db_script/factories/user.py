from __future__ import annotations

from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.dto import UserDTO

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        PasswordProvider,
        RandomBirthDateProvider,
        RandomTextProvider,
        RandomUserProfileProvider,
        RandomValueFromListProvider,
    )


class UserFactory:
    """Contains methods for generating values for UserDTO."""

    def __init__(
        self,
        random_country_provider: RandomValueFromListProvider,
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

    def generate(self) -> UserDTO:
        """Generates random data for UserDTO"""

        profile = self._random_profile_provider()
        return UserDTO(
            description=self._random_text_provider(),
            country_id=self._random_country_provider(),
            birth_date=self._random_birth_date_provider(),
            username=profile["username"],
            first_name=profile["first_name"],
            last_name=profile["last_name"],
            email=profile["email"],
            is_active=True,
            encrypted_password=self._password_provider()["encrypted_password"],
            unencrypted_password=self._password_provider()["unencrypted_password"],
        )
