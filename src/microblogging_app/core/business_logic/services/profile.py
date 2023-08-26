from __future__ import annotations

import logging
from io import BytesIO
from sys import getsizeof
from typing import TYPE_CHECKING
from uuid import uuid4

from core.business_logic.dto import ProfileDTO
from core.business_logic.errors import (
    InvalidAuthCredentialsError,
    UserAlreadyExistsError,
)
from core.business_logic.services.registration import send_confirmation_email
from core.models import Country, Repost, Tweet
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.db.models import Count, Q
from PIL import Image

if TYPE_CHECKING:
    from core.business_logic.dto import EditProfileDTO
    from django.contrib.auth.models import AbstractBaseUser
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


def get_user_by_username(username: str) -> AbstractBaseUser:
    """Gets user object from DB by passed username."""

    user = (
        get_user_model()
        .objects.prefetch_related("following")
        .select_related("country")
        .annotate(followers_num=Count("followers", distinct=True), following_num=Count("following", distinct=True))
        .get(username=username)
    )
    return user


def get_user_tweets(user: AbstractBaseUser) -> QuerySet:
    """Gets user tweets from DB by passed user."""

    result = (
        Tweet.objects.select_related("user", "reply_to", "reply_to__user")
        .filter(user=user)
        .annotate(
            num_reposts=Count("reposts", distinct=True),
            num_likes=Count("likes", distinct=True),
            num_replies=Count("tweets_replies", distinct=True),
        )
        .prefetch_related("like", "repost", "tags")
        .order_by("-created_at")
    )
    return result


def get_user_tweets_with_reposts(user: AbstractBaseUser) -> QuerySet:
    """Gets user tweets from DB by passed user."""

    result = (
        Tweet.objects.annotate(
            num_reposts=Count("reposts", distinct=True),
            num_likes=Count("likes", distinct=True),
            num_replies=Count("tweets_replies", distinct=True),
        )
        .prefetch_related("like", "repost", "tags")
        .select_related("user", "reply_to", "reply_to__user")
        .filter(Q(user=user) | Q(reposts__user=user))
        .order_by("created_at")
    )
    return result


def get_user_reposts(user: AbstractBaseUser) -> QuerySet:
    """Gets user tweets with reposts from DB by passed user."""

    result = Repost.objects.select_related("tweet", "user").filter(user=user)
    return result


def get_profile_info(username: str) -> ProfileDTO:
    """Gets info about user and his tweets from DB."""

    user = get_user_by_username(username=username)
    user_tweets = get_user_tweets(user=user)
    profile = ProfileDTO(
        user=user,
        user_tweets=user_tweets,
    )
    return profile


def get_profile_with_reposts_info(username: str) -> ProfileDTO:
    """Gets info about user and his tweets from DB."""

    user = get_user_by_username(username=username)
    user_tweets = get_user_tweets_with_reposts(user=user)
    user_reposts = get_user_reposts(user=user)
    profile = ProfileDTO(user=user, user_tweets=user_tweets, user_reposts=user_reposts)
    return profile


def replace_file_name_to_uuid(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    """Replaces the user's filename with the uuid4 standard name."""

    old_name = file.name
    file_extension = old_name.split(".")[-1]
    file_name = str(uuid4())
    file.name = file_name + "." + file_extension
    logger.info(
        "Successfully replaced file name with the uuid4 standard name",
        extra={"old_file_name": old_name, "new_file_name": file.name},
    )
    return file


def change_file_size(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    """Changes the size of uploaded images."""

    content_type = file.content_type
    if content_type is not None:
        file_format = content_type.split("/")[-1].upper()
    else:
        file_format = ""
    output = BytesIO()
    with Image.open(file) as image:
        image.thumbnail(size=(400, 400))
        image.save(output, format=file_format, quality=100)
    old_size = file.size
    new_size = getsizeof(output)
    file = InMemoryUploadedFile(
        file=output,
        field_name=file.field_name,
        name=file.name,
        content_type=file.content_type,
        size=getsizeof(output),
        charset=file.charset,
    )
    logger.info("Successfully changed file size", extra={"old_size": str(old_size), "new_size": str(new_size)})
    return file


def edit_profile(data: EditProfileDTO) -> None:
    """Edits user profile."""

    user = get_user_model().objects.get(pk=data.user_id)
    country = Country.objects.get(name=data.country)
    try:
        if data.photo is not None:
            file = replace_file_name_to_uuid(data.photo)
            file = change_file_size(file=file)
            user.photo = file
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.username = data.username
        user.birth_date = data.birth_date
        user.description = data.description
        user.country = country
        user.email = data.email
        user.save()
    except IntegrityError:
        logger.info(
            msg="Such email or username already exist.",
            extra={"user_email": data.email, "username": data.username},
        )
        raise UserAlreadyExistsError
    if data.old_password and data.new_password:
        if user.check_password(data.old_password):
            user.set_password(data.new_password)
        else:
            raise InvalidAuthCredentialsError
    if data.old_email != data.email:
        user.is_active = False
        send_confirmation_email(user=user)
        user.save()
    logger.info(msg="User profile is updated.", extra={"user_id": data.user_id})
