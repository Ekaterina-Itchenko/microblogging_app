from typing import TYPE_CHECKING

from core.business_logic.errors import UnauthorizedAction
from core.business_logic.services import (
    create_tweet,
    get_reposts_from_following_users,
    get_tweet_and_replies,
    get_tweets_from_following_users,
    like_tweet,
    repost_tweet,
)
from core.models import Tweet
from core.presentation_layer.forms import TweetForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest


@require_http_methods(request_method_list=["GET", "POST"])
def index_controller(request: HttpRequest) -> HttpResponse:
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

    form = TweetForm()
    if request.method == "POST":
        form = TweetForm(data=request.POST)
        if form.is_valid():
            tweet_data = form.cleaned_data
            tweet_data["user"] = user
            create_tweet(data=tweet_data)
            return HttpResponseRedirect(reverse("index"))

    context = {
        "tweets": following_tweets + following_reposts,
        "form": form,
        "order_by": order_by,
    }
    return render(request, "home.html", context)


@require_http_methods(request_method_list=["GET"])
def tweet_detail_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    tweet, replies = get_tweet_and_replies(tweet_id)
    context = {
        "tweet": tweet,
        "replies": replies,
    }
    return render(request, "tweet_detail.html", context)


@require_http_methods(request_method_list=["POST"])
def like_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    user = request.user  # Assuming users are properly authenticated
    if not user.is_authenticated:
        return HttpResponseBadRequest("You must be logged in to like a tweet.")
    try:
        tweet = Tweet.objects.get(pk=tweet_id)
        like_tweet(user, tweet)
        return HttpResponse(status=200)
    except (Tweet.DoesNotExist, UnauthorizedAction) as e:
        return HttpResponseBadRequest(str(e))


@require_http_methods(request_method_list=["POST"])
def repost_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    user = request.user  # Assuming users are properly authenticated
    if not user.is_authenticated:
        return HttpResponseBadRequest("You must be logged in to repost a tweet.")
    try:
        tweet = Tweet.objects.get(pk=tweet_id)
        repost_tweet(user, tweet)
        return HttpResponse(status=200)
    except (Tweet.DoesNotExist, UnauthorizedAction) as e:
        return HttpResponseBadRequest(str(e))
