from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.errors import TweetNotFound, UnauthorizedAction
from core.business_logic.services import like_tweet
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = logging.getLogger(__name__)


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
        return redirect(to=request.META.get("HTTP_REFERER"))
    except TweetNotFound:
        return HttpResponseBadRequest("Tweet doesn't found.")
    except UnauthorizedAction:
        return HttpResponseBadRequest("You can't like a tweet created by yourself.")
