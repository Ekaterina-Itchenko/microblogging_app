"""
"Core" app Tag model of microblogging_app project.
"""

from django.db import models

from .base import BaseModel


class Tag(BaseModel):
    """Describes the fields and attributes of the Tag model in the database."""

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        """Describes class metadata."""

        db_table = "tags"
