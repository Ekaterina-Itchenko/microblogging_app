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

    description = models.CharField(max_length=400)
    photo = models.ImageField(upload_to=user_photo_directory_path, null=True)
    birth_date = models.DateField()
    country = models.ForeignKey(to="Country", on_delete=models.CASCADE, related_name="users", null=True)
    followers = models.ManyToManyField(to="self", db_table="followers", symmetrical=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        """Describes class metadata."""

        db_table = "users"
