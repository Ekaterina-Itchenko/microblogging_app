from dataclasses import dataclass
from typing import Optional

from django.contrib.auth.models import AbstractBaseUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet


@dataclass
class ProfileDTO:
    """Data transfer object for storing and transferring data to profile view."""

    user: AbstractBaseUser
    user_tweets: QuerySet
    user_reposts: Optional[QuerySet] = None


@dataclass
class EditProfileDTO:
    """Data transfer object for storing and transferring data from EditProfileForm."""

    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    old_email: str
    email: str
    birth_date: object
    description: Optional[str]
    country: str
    old_password: str
    new_password: str
    user_id: int
    photo: Optional[InMemoryUploadedFile]
