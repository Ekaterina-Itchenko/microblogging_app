from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.core.files import File

if TYPE_CHECKING:
    from datetime import date


def is_leap(year: int) -> bool:
    """Function to determine if a year is a leap year"""
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False


class ValidateUserAge:
    """Validate user age. Minimal age should be set."""

    def __init__(self, min_age: int) -> None:
        self._min_age = min_age

    def __call__(self, value: date) -> None:
        current_date = datetime.now().date()
        leap_years: int = 0
        for year in range(value.year, current_date.year + 1):
            if is_leap(year=year):
                leap_years += 1
        age = (datetime.now().date() - value) - timedelta(days=leap_years)
        if age.days / 365 < self._min_age:
            raise ValidationError(message=f"Available age for registration is {self._min_age}")
        else:
            return None


class ValidateMaxTagCount:
    """Validates the number of tags."""

    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> None:
        number_of_tags = len(value.split("\r\n"))

        if number_of_tags > self._max_count:
            raise ValidationError(message=f"Max number of tags is {self._max_count}")


class ValidateFileSize:
    """Validates file size."""

    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, value: File) -> None:
        file_size = value.size
        if file_size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            raise ValidationError(message=f"Max file size is {max_size_in_mb} MB.")


class ValidateImageExtensions:
    """Validates image extensions."""

    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> None:
        image_extensions = value.name.split(".")[-1]
        if image_extensions not in self._available_extensions:
            raise ValidationError(message=f"Accept only {self._available_extensions}.")
