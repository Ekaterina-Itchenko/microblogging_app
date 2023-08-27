from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.services import (
    follow_user,
    unfollow_user,
    user_followers,
    user_following,
)
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = logging.getLogger(__name__)


@query_debugger
@require_http_methods(request_method_list=["POST"])
def follow_controller(request: HttpRequest, username: str) -> HttpResponse:
    """Follow user with passed ID controller."""

    user = request.user
    if not user.is_authenticated:
        logger.warning("Unauthorized attempt to follow user.")
        return HttpResponseBadRequest("You must be logged in to follow a another user.")

    follow_user(user, followed_user_username=username)
    return redirect(to=request.META.get("HTTP_REFERER"))


@query_debugger
@require_POST
def unfollow_controller(request: HttpRequest, username: str) -> HttpResponse:
    """Unfollow user with passed ID controller."""

    user = request.user
    if not user.is_authenticated:
        logger.warning("Unauthorized attempt to unfollow user.")
        return HttpResponseBadRequest("You must be logged in to unfollow another user.")

    unfollow_user(user, followed_user_username=username)
    return redirect(to=request.META.get("HTTP_REFERER"))


@query_debugger
@require_GET
def followers_controller(request: HttpRequest, username: str) -> HttpResponse:
    """User followers controller."""

    authorized_user_dto = user_following(request.user.username)
    auth_user_following = authorized_user_dto.following
    followers_dto = user_followers(user_username=username)
    followers = followers_dto.followers
    fullname = followers_dto.user_fullname
    context = {
        "followers": followers,
        "user_fullname": fullname,
        "user_username": username,
        "auth_user_following": auth_user_following,
        "followers_num": followers_dto.followers_num,
        "following_num": followers_dto.following_num,
    }
    return render(request=request, template_name="followers.html", context=context)


@query_debugger
@require_GET
def following_controller(request: HttpRequest, username: str) -> HttpResponse:
    """User following controller."""

    authorized_user_dto = user_following(request.user.username)
    auth_user_following = authorized_user_dto.following
    auth_user_fullname = authorized_user_dto.user_fullname
    if username == request.user.username:
        following_dto = authorized_user_dto
        following = auth_user_following
        fullname = auth_user_fullname
    else:
        following_dto = user_following(user_username=username)
        following = following_dto.following
        fullname = following_dto.user_fullname
    context = {
        "following": following,
        "user_fullname": fullname,
        "user_username": username,
        "auth_user_following": auth_user_following,
        "followers_num": following_dto.followers_num,
        "following_num": following_dto.following_num,
    }
    return render(request=request, template_name="following.html", context=context)
