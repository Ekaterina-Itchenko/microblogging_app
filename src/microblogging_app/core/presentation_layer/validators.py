from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError

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


class TagsNumberValidator:
    def __init__(self, max_number: int) -> None:
        self.max_number = max_number

    def __call__(self, value: str) -> None:
        number = len(value.split("\r\n"))
        if number > self.max_number:
            raise ValidationError(message=f"Maximal number of tags is {self.max_number}")
        else:
            return None
