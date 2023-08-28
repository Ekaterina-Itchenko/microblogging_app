"""
"Core" app User model of microblogging_app project.
"""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models

from .base import BaseModel


def user_photo_directory_path(instance: "User", filename: str) -> str:
    """Provides a path to directory with files of user."""

    return f"users_media/{instance.username}/{filename}"


class User(BaseModel, AbstractUser):
    """Describes the fields and attributes of the User model in the database."""

    description = models.CharField(max_length=400, blank=True)
    photo = models.ImageField(upload_to=user_photo_directory_path, null=True, blank=True)
    birth_date = models.DateField()
    country = models.ForeignKey(to="Country", on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    following = models.ManyToManyField(
        to="self", db_table="followers", symmetrical=False, related_name="followers", blank=True
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        """Describes class metadata."""

        db_table = "users"
