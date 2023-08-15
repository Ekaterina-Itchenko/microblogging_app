import logging
from typing import List, Optional, Tuple

from core.business_logic.errors import TweetNotFound, UnauthorizedAction
from core.models import Tweet, User
from django.db import transaction

logger = logging.getLogger(__name__)


class TweetData:
    def __init__(self, user: User, content: str, reply_to: Optional[Tweet] = None, reply_counter: int = 0):
        self.user = user
        self.content = content
        self.reply_to = reply_to
        self.reply_counter = reply_counter


def create_tweet(data: TweetData) -> None:
    with transaction.atomic():
        Tweet.objects.create(
            user=data.user, content=data.content, reply_to=data.reply_to, reply_counter=data.reply_counter
        )
        if data.reply_to:
            data.reply_to.reply_counter += 1
            data.reply_to.save()


def get_user_tweets(user: User) -> List[Tweet]:
    return list(Tweet.objects.filter(user=user).order_by("-created_at"))


def get_tweet_and_replies(tweet_id: int) -> Tuple[Tweet, List[Tweet]]:
    try:
        tweet = Tweet.objects.get(pk=tweet_id)
    except Tweet.DoesNotExist as err:
        logger.error("Tweet not found.", extra={"tweet_id": tweet_id}, exc_info=err)
        raise TweetNotFound

    replies = list(Tweet.objects.filter(reply_to=tweet).order_by("created_at"))
    return tweet, replies


def get_tweets_from_following_users(user: User) -> List[Tweet]:
    following_users = user.followers.all()
    return list(Tweet.objects.filter(user__in=following_users).order_by("-created_at"))


def get_reposts_from_following_users(user: User) -> List[Tweet]:
    following_users = user.followers.all()
    return list(Tweet.objects.filter(repost__user__in=following_users).order_by("-created_at"))


def like_tweet(user: User, tweet: Tweet) -> None:
    if tweet.user == user:
        raise UnauthorizedAction("Cannot like own tweet")
    tweet.like.add(user)


def repost_tweet(user: User, tweet: Tweet) -> None:
    if tweet.user == user:
        raise UnauthorizedAction("Cannot repost own tweet")
    tweet.repost.add(user)
