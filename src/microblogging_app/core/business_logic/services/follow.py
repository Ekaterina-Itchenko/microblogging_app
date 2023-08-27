from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import FollowersDTO, FollowingDTO
from django.contrib.auth import get_user_model
from django.db.models import Count

if TYPE_CHECKING:
    from core.models import User
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


def follow_user(user: User, followed_user_username: str) -> None:
    """Adds an authorized user to the followers of user with passed ID."""

    followed_user = get_user_model().objects.prefetch_related("followers").get(username=followed_user_username)
    followed_user.followers.add(user)
    logger.info(f"User '{user.username}' follow user {followed_user.username}.")


def unfollow_user(user: User, followed_user_username: str) -> None:
    """Removes an authorized user from the followers of user with passed ID."""

    followed_user = get_user_model().objects.prefetch_related("followers").get(username=followed_user_username)
    followed_user.followers.remove(user)
    logger.info(f"User '{user.username}'unfollow user {followed_user.username}.")


def user_followers(user_username: str) -> FollowersDTO:
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


def user_following(user_username: str) -> FollowingDTO:
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
