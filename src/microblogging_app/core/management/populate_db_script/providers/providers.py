"""
Contains Providers classes that generates random data for populating database.
"""

from random import choice, randint
from typing import TYPE_CHECKING, Optional

from django.contrib.auth.hashers import PBKDF2PasswordHasher
from faker import Faker

if TYPE_CHECKING:
    from datetime import date

fake_data = Faker()


class RandomObjectFromListProvider:
    """Provider that selects random object from list."""

    def __init__(self, values: list[object]) -> None:
        self._values = values

    def __call__(self) -> object:
        random_obj = choice(self._values)
        return random_obj


class RandomDistinctObjectFromListProvider:
    """Provider that selects random object from list other than the one passed during the call."""

    def __init__(self, values: list[object]) -> None:
        self._values = values

    def __call__(self, value: object) -> object:
        random_value = choice(self._values)
        if random_value == value:
            return self.__call__(value=value)
        else:
            return random_value


class RandomObjectFromListOrNoneProvider:
    """Provider that generates random value from list."""

    def __init__(self, values: list[object]) -> None:
        self._values = values

    def __call__(self) -> Optional[object]:
        if len(self._values) == 0:
            return None
        else:
            random_value = choice(self._values)
            final_result: Optional[object] = choice([random_value, None])
            return final_result


class NotificationMessageProvider:
    """Provider that generates notifications messages."""

    def __call__(self) -> str:
        message = fake_data.text(max_nb_chars=randint(50, 360))
        result_message = f"Test Admin Notification: {message}"
        return result_message


class RandomTagProvider:
    """Provider that generates random Tag."""

    def __call__(self) -> str:
        random_tag: str = fake_data.word()
        return random_tag


class RandomTextProvider:
    """Provider that generates random text."""

    def __init__(self, max_length: int) -> None:
        self._max_length = max_length

    def __call__(self) -> str:
        random_text: str = fake_data.text(max_nb_chars=self._max_length)
        return random_text


class RandomBirthDateProvider:
    """Provider that generates random birth date.

    Users with generated birth dates are over 18 and under 90 years old."""

    def __call__(self) -> "date":
        random_date: date = fake_data.date_of_birth(minimum_age=18, maximum_age=90)
        return random_date


class RandomUserProfileProvider:
    """Generates random username, first name, last name, and email of user."""

    def __call__(self) -> dict[str, str]:
        random_profile: dict = fake_data.simple_profile()
        username: str = random_profile["username"]
        first_name: str = random_profile["name"].split()[-2]
        last_name: str = random_profile["name"].split()[-1]
        mail: str = random_profile["mail"]
        result_profile: dict[str, str] = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": mail,
        }
        return result_profile


class PasswordProvider:
    """Generates a hashed password in the format used by django application.

    By default, the password is set to 'password123'
    To generate passwords, the class "PBKDF2PasswordHasher" from "django.contrib.auth.hashers" is used, since user
    passwords in the database must be hashed in the same way as in the django application that uses this data.
    """

    def __init__(self, unencrypted_password: str = "password123") -> None:
        self._unencrypted_password = unencrypted_password

    def __call__(self) -> str:
        hasher = PBKDF2PasswordHasher()
        salt = hasher.salt()
        encrypted_password: str = hasher.encode(password=self._unencrypted_password, salt=salt)
        return encrypted_password
