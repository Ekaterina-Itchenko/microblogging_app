"""
"Core" app Country model of microblogging_app project.
"""

from django.db import models

from .base import BaseModel


class Country(BaseModel):
    """Describes the fields and attributes of the Country model in the database."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        """Describes class metadata."""

        db_table = "countries"
