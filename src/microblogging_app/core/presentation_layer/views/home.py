from typing import TYPE_CHECKING

from core.presentation_layer.pagination import CustomPagination, PageNotExists

if TYPE_CHECKING:
    from django.http import HttpRequest

import logging

from core.business_logic.errors import UnauthorizedAction
from core.business_logic.services import (
    get_reposts_from_following_users,
    get_tweet_and_replies,
    get_tweets_from_following_users,
    like_tweet,
    repost_tweet,
)
from core.models import Tweet
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


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
        following_tweets = get_tweets_from_following_users(user)
        following_reposts = get_reposts_from_following_users(user)
    else:
        following_tweets = []
        following_reposts = []

    order_by = request.GET.get("order_by", "newest")
    if order_by == "most_likes":
        following_tweets = sorted(following_tweets, key=lambda tweet: tweet.number_of_likes(), reverse=True)

    combined_tweets = following_tweets + following_reposts

    # Apply custom pagination
    page_number = request.GET.get("page", 1)
    paginator = CustomPagination(per_page=20)
    try:
        tweets_paginated = paginator.paginate(data=combined_tweets, page_number=page_number)
    except PageNotExists:
        return HttpResponseBadRequest("Page with provided number doesn't exist.")

    context = {
        "tweets": tweets_paginated.data,
        "order_by": order_by,
        "next_page": tweets_paginated.next_page,
        "prev_page": tweets_paginated.prev_page,
    }
    return render(request, "home.html", context)


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

    tweet = get_object_or_404(Tweet, pk=tweet_id)
    tweet, replies = get_tweet_and_replies(tweet_id)
    context = {
        "tweet": tweet,
        "replies": replies,
    }
    return render(request, "tweet_detail.html", context)


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

    user = request.user  # Assuming users are properly authenticated
    if not user.is_authenticated:
        logger.warning("Unauthorized attempt to like a tweet.")
        return HttpResponseBadRequest("You must be logged in to like a tweet.")
    try:
        tweet = Tweet.objects.get(pk=tweet_id)
        like_tweet(user, tweet)
        logger.info(f"User '{user.username}' liked tweet with ID {tweet_id}.")
        return redirect("home")
    except (Tweet.DoesNotExist, UnauthorizedAction) as err:
        logger.error(f"Error while liking tweet with ID {tweet_id}: {err}")
        return HttpResponseBadRequest(str(err))


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
    user = request.user  # Assuming users are properly authenticated
    if not user.is_authenticated:
        logger.warning("Unauthorized attempt to repost a tweet.")
        return HttpResponseBadRequest("You must be logged in to repost a tweet.")
    try:
        tweet = Tweet.objects.get(pk=tweet_id)
        repost_tweet(user, tweet)
        logger.info(f"User '{user.username}' reposted tweet with ID {tweet_id}.")
        return redirect("home")
    except (Tweet.DoesNotExist, UnauthorizedAction) as err:
        logger.error(f"Error while reposting tweet with ID {tweet_id}: {err}")
        return HttpResponseBadRequest(str(err))
