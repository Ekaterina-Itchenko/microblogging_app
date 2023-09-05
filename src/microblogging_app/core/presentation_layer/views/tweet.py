from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import AddTweetDTO, EditTweetDTO
from core.business_logic.services import (
    create_tweet,
    edit_tweet,
    get_replies,
    get_tweet_info,
)
from core.presentation_layer.converters import convert_data_from_form_to_dto
from core.presentation_layer.forms import AddTweetForm, EditTweetForm
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@query_debugger
@require_http_methods(request_method_list=["GET"])
def tweet_detail_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    """
    Display the detail page of a tweet and its replies.
    Args:
        request: The HTTP request.
        tweet_id: The ID of the tweet to display.
    Returns:
        HttpResponse: The rendered tweet detail page.
    """

    tweet = get_tweet_info(tweet_id)
    replies = get_replies(tweet_id)
    context = {
        "tweet": tweet,
        "replies": replies,
    }
    return render(request, "tweet_detail.html", context)


@query_debugger
@require_http_methods(request_method_list=["GET"])
def tweet_detail_controller_likes(request: HttpRequest, tweet_id: int) -> HttpResponse:
    """
    Display the detail page of a tweet and users who like it.
    Args:
        request: The HTTP request.
        tweet_id: The ID of the tweet to display.
    Returns:
        HttpResponse: The rendered tweet detail likes page.
    """

    tweet = get_tweet_info(tweet_id)
    auth_user_following = request.user.following.all()
    context = {"tweet": tweet, "auth_user_following": auth_user_following}
    return render(request, "tweet_detail_likes.html", context)


@query_debugger
@require_http_methods(request_method_list=["GET"])
def tweet_detail_controller_reposts(request: HttpRequest, tweet_id: int) -> HttpResponse:
    """
    Display the detail page of a tweet and users who like it.
    Args:
        request: The HTTP request.
        tweet_id: The ID of the tweet to display.
    Returns:
        HttpResponse: The rendered tweet detail likes page.
    """

    tweet = get_tweet_info(tweet_id)
    auth_user_following = request.user.following.all()
    context = {"tweet": tweet, "auth_user_following": auth_user_following}
    return render(request, "tweet_detail_reposts.html", context)


@query_debugger
@require_http_methods(["GET", "POST"])
def add_tweet_controller(request: HttpRequest) -> HttpResponse:
    """Add tweet controller."""
    if request.method == "GET":
        form = AddTweetForm()
        context = {"form": form}
        logger.info("rendered form")
        return render(request=request, template_name="add_tweet.html", context=context)
    if request.method == "POST":
        form = AddTweetForm(request.POST)
        if form.is_valid():
            logger.info("form is valid")
            data = convert_data_from_form_to_dto(dto=AddTweetDTO, data_from_form=form.cleaned_data)
            data.user = request.user
            create_tweet(data=data)
            return redirect(to="profile", username=request.user.username)
        else:
            logger.info("Invalid form", extra={"post_data": request.POST})
    return HttpResponseBadRequest("Incorrect HTTP method.")


@query_debugger
@require_http_methods(["GET", "POST"])
def edit_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    """Add tweet controller."""

    edited_tweet = get_tweet_info(tweet_id=tweet_id)
    edited_content = edited_tweet.content
    edited_tags = " ".join([tag.name for tag in edited_tweet.tags.all()])
    edited_tweet_data = {"content": edited_content, "tags": edited_tags, "tweet_id": edited_tweet.pk}
    if request.method == "GET":
        form = EditTweetForm(initial=edited_tweet_data)
        context = {"form": form, "tweet_id": edited_tweet.pk}
        logger.info("rendered form")
        return render(request=request, template_name="edit_tweet.html", context=context)
    if request.method == "POST":
        form = EditTweetForm(request.POST)
        if form.is_valid():
            logger.info("form is valid")
            data = convert_data_from_form_to_dto(dto=EditTweetDTO, data_from_form=form.cleaned_data)
            edit_tweet(data=data)
            return redirect(to="profile", username=request.user.username)
        else:
            logger.info("Invalid form", extra={"post_data": request.POST})
    return HttpResponseBadRequest("Incorrect HTTP method.")
