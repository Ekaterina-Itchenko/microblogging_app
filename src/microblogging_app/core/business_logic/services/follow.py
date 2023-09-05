from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import (
    FollowersDTO,
    FollowersPageDTO,
    FollowingDTO,
    FollowingPageDTO,
)
from django.contrib.auth import get_user_model
from django.db.models import Count

if TYPE_CHECKING:
    from core.models import User
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


def follow_user(authorized_user: User, followed_user_username: str) -> None:
    """Adds an authorized user to the followers of user with passed ID."""

    followed_user = get_user_model().objects.prefetch_related("followers").get(username=followed_user_username)
    followed_user.followers.add(authorized_user)
    logger.info(f"User '{authorized_user.username}' follow user {followed_user.username}.")


def unfollow_user(authorized_user: User, followed_user_username: str) -> None:
    """Removes an authorized user from the followers of user with passed ID."""

    followed_user = get_user_model().objects.prefetch_related("followers").get(username=followed_user_username)
    followed_user.followers.remove(authorized_user)
    logger.info(f"User '{authorized_user.username}'unfollow user {followed_user.username}.")


def user_followers_by_username(user_username: str) -> FollowersDTO:
    """Returns QuerySet with followers of the user with passed ID."""

    user = (
        get_user_model()
        .objects.prefetch_related("followers")
        .annotate(followers_num=Count("followers", distinct=True), following_num=Count("following", distinct=True))
        .get(username=user_username)
    )
    followers: QuerySet = user.followers.all()
    followers_dto = FollowersDTO(
        user_fullname=(f"{user.first_name} {user.last_name}"),
        followers=followers,
        followers_num=user.followers_num,
        following_num=user.following_num,
    )

    return followers_dto


def user_following_by_username(user_username: str) -> FollowingDTO:
    """Returns QuerySet with following users of the user with passed ID."""

    user = (
        get_user_model()
        .objects.prefetch_related("following")
        .annotate(followers_num=Count("followers", distinct=True), following_num=Count("following", distinct=True))
        .get(username=user_username)
    )
    following: QuerySet = user.following.all()
    following_dto = FollowingDTO(
        user_fullname=(f"{user.first_name} {user.last_name}"),
        following=following,
        followers_num=user.followers_num,
        following_num=user.following_num,
    )
    return following_dto


def get_followers_page_data(user_username: str, auth_user: User) -> FollowersPageDTO:
    """Returns DTO with data for render followers_page."""

    authorized_user_dto = user_following_by_username(auth_user.username)
    auth_user_following = authorized_user_dto.following
    followers_dto = user_followers_by_username(user_username=user_username)
    followers = followers_dto.followers
    fullname = followers_dto.user_fullname
    result = FollowersPageDTO(
        followers=followers,
        user_fullname=fullname,
        user_username=user_username,
        auth_user_following=auth_user_following,
        followers_num=followers_dto.followers_num,
        following_num=followers_dto.following_num,
    )
    return result


def get_following_page_data(user_username: str, auth_user: User) -> FollowingPageDTO:
    """Returns DTO with data for render following page."""

    authorized_user_dto = user_following_by_username(auth_user.username)
    auth_user_following = authorized_user_dto.following
    auth_user_fullname = authorized_user_dto.user_fullname
    if user_username == auth_user.username:
        following_dto = authorized_user_dto
        following = auth_user_following
        fullname = auth_user_fullname
    else:
        following_dto = user_following_by_username(user_username=user_username)
        following = following_dto.following
        fullname = following_dto.user_fullname

    result = FollowingPageDTO(
        following=following,
        user_fullname=fullname,
        user_username=user_username,
        auth_user_following=auth_user_following,
        followers_num=following_dto.followers_num,
        following_num=following_dto.following_num,
    )
    return result
