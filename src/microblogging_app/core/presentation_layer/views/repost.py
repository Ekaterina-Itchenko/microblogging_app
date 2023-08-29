from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.services import repost_tweet
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = logging.getLogger(__name__)


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
        logger.warning("Unauthorized attempt to like a tweet.")
        return HttpResponseBadRequest("You must be logged in to repost a tweet.")

    repost_tweet(user, tweet_id)
    return redirect(to=request.META.get("HTTP_REFERER"))
