from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import AddTweetDTO
from core.business_logic.errors import TweetNotFound
from core.business_logic.services import create_tweet, get_tweet_info
from core.presentation_layer.converters import convert_data_from_form_to_dto
from core.presentation_layer.forms import AddTweetForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = logging.getLogger(__name__)


@query_debugger
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
        form = AddTweetForm()
        replied_tweet = get_tweet_info(tweet_id=tweet_id)
        context = {"form": form, "replied_tweet": replied_tweet}
        return render(request=request, template_name="reply_tweet.html", context=context)
    if request.method == "POST":
        form = AddTweetForm(request.POST)
        if form.is_valid():
            received_data: AddTweetDTO = convert_data_from_form_to_dto(AddTweetDTO, form.cleaned_data)
            received_data.user = request.user
            received_data.reply_to_id = tweet_id
            try:
                create_tweet(data=received_data)
            except TweetNotFound:
                return HttpResponseBadRequest(content="The tweet you want to reply doesn't exist.")
            return redirect(to="tweet_detail", tweet_id=tweet_id)
        else:
            context = {"form": form, "replied_tweet": replied_tweet}
            return render(request=request, template_name="reply_tweet.html", context=context)
    return HttpResponseBadRequest("Incorrect HTTP method.")
