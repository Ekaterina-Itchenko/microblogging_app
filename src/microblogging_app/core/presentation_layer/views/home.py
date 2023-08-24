from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import TweetDTO
from core.business_logic.errors import (
    TweetAlreadyLikedByUserError,
    TweetAlreadyRepostedByUserError,
    TweetNotFound,
    UnauthorizedAction,
)
from core.business_logic.services import (
    create_tweet,
    get_replies,
    get_tweet,
    get_tweets_reposts_from_following_users,
    like_tweet,
    ordering_tweets,
    repost_tweet,
)
from core.presentation_layer.converters import convert_data_from_form_to_dto
from core.presentation_layer.forms import TweetForm
from core.presentation_layer.pagination import CustomPagination, PageNotExists
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


@query_debugger
@require_http_methods(request_method_list=["GET", "POST"])
def index_controller(request: HttpRequest) -> HttpResponse:
    """
    Display the home page containing tweets and handling tweet creation.

    Args:
        request: The HTTP request.

    Returns:
        HttpResponse: The rendered home page.
    """

    user = request.user

    if user.is_authenticated:
        tweets = get_tweets_reposts_from_following_users(user)
    else:
        return redirect(to="sign_in")

    order_by = request.GET.get("order_by", "newest")
    ordered_tweets = ordering_tweets(tweets=tweets, condition=order_by)

    # Apply custom pagination
    page_number = request.GET.get("page", 1)
    paginator = CustomPagination(per_page=20)
    try:
        tweets_paginated = paginator.paginate(data=ordered_tweets, page_number=page_number)
    except PageNotExists:
        return HttpResponseBadRequest("Page with provided number doesn't exist.")

    context = {
        "tweets": tweets_paginated.data,
        "order_by": order_by,
        "next_page": tweets_paginated.next_page,
        "prev_page": tweets_paginated.prev_page,
    }
    return render(request, "home.html", context)


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

    tweet = get_tweet(tweet_id)
    replies = get_replies(tweet_id)
    context = {
        "tweet": tweet,
        "replies": replies,
    }
    return render(request, "tweet_detail.html", context)


@query_debugger
@require_http_methods(request_method_list=["POST"])
def like_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    """
    Like a tweet.
    Args:
        request: The HTTP request.
        tweet_id: The ID of the tweet to like.
    Returns:
        HttpResponse: A response indicating the result of the action.
    """

    user = request.user
    if not user.is_authenticated:
        logger.warning("Unauthorized attempt to like a tweet.")
        return HttpResponseBadRequest("You must be logged in to like a tweet.")
    try:
        like_tweet(user, tweet_id)
        logger.info(f"User '{user.pk}' liked tweet with ID {tweet_id}.")
        return redirect("home")
    except TweetNotFound:
        return HttpResponseBadRequest("Tweet doesn't found.")
    except UnauthorizedAction:
        return HttpResponseBadRequest("You can't like a tweet created by yourself.")
    except TweetAlreadyLikedByUserError:
        return HttpResponseBadRequest("You have already liked this tweet earlier. You couldn't do it again")


@query_debugger
@require_http_methods(request_method_list=["POST"])
def repost_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    """
    Repost a tweet.
    Args:
        request: The HTTP request.
        tweet_id: The ID of the tweet to repost.
    Returns:
        HttpResponse: A response indicating the result of the action.
    """

    user = request.user
    if not user.is_authenticated:
        logger.warning("Unauthorized attempt to repost a tweet.")
        return HttpResponseBadRequest("You must be logged in to repost a tweet.")
    try:
        repost_tweet(user=user, tweet_id=tweet_id)
        logger.info(f"User '{user.pk}' reposted tweet with ID {tweet_id}.")
        return redirect("home")
    except TweetNotFound:
        return HttpResponseBadRequest("Tweet doesn't found.")
    except UnauthorizedAction:
        return HttpResponseBadRequest("You can't repost a tweet created by yourself.")
    except TweetAlreadyRepostedByUserError:
        return HttpResponseBadRequest("You have already reposted this tweet earlier. You couldn't do it again")


@require_http_methods(request_method_list=["GET", "POST"])
def reply_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    """
    Reply to a tweet.
    Args:
        request: The HTTP request.
        tweet_id: The ID of the tweet.
    Returns:
        HttpResponse: A response indicating the result of the action.
    """

    user = request.user
    if not user.is_authenticated:
        logger.warning("Unauthorized attempt to reply to a tweet.")
        return HttpResponseBadRequest("You must be logged in to reply to a tweet.")

    if request.method == "GET":
        form = TweetForm()
        context = {"form": form, "tweet_id": tweet_id}
        return render(request=request, template_name="create_tweet.html", context=context)
    else:
        form = TweetForm(request.POST)
        if form.is_valid():
            received_data = convert_data_from_form_to_dto(TweetDTO, form.cleaned_data)
            try:
                create_tweet(data=received_data, user=user, reply_to=tweet_id)
            except TweetNotFound:
                return HttpResponseBadRequest(content="The tweet you want to reply to doesn't exist.")
            return redirect(to="home")
        else:
            context = {"form": form, "tweet_id": tweet_id}
            return render(request=request, template_name="create_tweet.html", context=context)
