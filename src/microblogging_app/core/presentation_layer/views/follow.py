from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.services import (
    follow_user,
    get_followers_page_data,
    get_following_page_data,
    unfollow_user,
)
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = logging.getLogger(__name__)


@require_http_methods(request_method_list=["POST"])
def follow_controller(request: HttpRequest, username: str) -> HttpResponse:
    """Follow user with passed ID controller."""

    user = request.user
    if not user.is_authenticated:
        logger.warning("Unauthorized attempt to follow user.")
        return HttpResponseBadRequest("You must be logged in to follow a another user.")

    follow_user(user, followed_user_username=username)
    return redirect(to=request.META.get("HTTP_REFERER"))


@require_POST
def unfollow_controller(request: HttpRequest, username: str) -> HttpResponse:
    """Unfollow user with passed ID controller."""

    user = request.user
    if not user.is_authenticated:
        logger.warning("Unauthorized attempt to unfollow user.")
        return HttpResponseBadRequest("You must be logged in to unfollow another user.")

    unfollow_user(user, followed_user_username=username)
    return redirect(to=request.META.get("HTTP_REFERER"))


@require_GET
def followers_controller(request: HttpRequest, username: str) -> HttpResponse:
    """User followers controller."""

    followers_controller_data = get_followers_page_data(user_username=username, auth_user=request.user)
    context = {
        "followers": followers_controller_data.followers,
        "user_fullname": followers_controller_data.user_fullname,
        "user_username": followers_controller_data.user_username,
        "auth_user_following": followers_controller_data.auth_user_following,
        "followers_num": followers_controller_data.followers_num,
        "following_num": followers_controller_data.following_num,
    }
    return render(request=request, template_name="followers.html", context=context)


@require_GET
def following_controller(request: HttpRequest, username: str) -> HttpResponse:
    """User following controller."""

    following_controller_data = get_following_page_data(user_username=username, auth_user=request.user)
    context = {
        "following": following_controller_data.following,
        "user_fullname": following_controller_data.user_fullname,
        "user_username": following_controller_data.user_username,
        "auth_user_following": following_controller_data.auth_user_following,
        "followers_num": following_controller_data.followers_num,
        "following_num": following_controller_data.following_num,
    }
    return render(request=request, template_name="following.html", context=context)
