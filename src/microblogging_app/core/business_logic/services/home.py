import logging
from typing import List, Tuple

from core.business_logic.dto.home import TweetDTO
from core.business_logic.errors import TweetNotFound, UnauthorizedAction
from core.models import Tweet, User
from django.db import transaction

logger = logging.getLogger(__name__)


def create_tweet(data: TweetDTO) -> None:
    """
    Create a new tweet and update reply count if it's a reply.

    Args:
        data (TweetData): Data containing tweet information.

    Returns:
        None
    """
    with transaction.atomic():
        Tweet.objects.create(
            user=data.user, content=data.content, reply_to=data.reply_to, reply_counter=data.reply_counter
        )
        if data.reply_to:
            data.reply_to.reply_counter += 1
            data.reply_to.save()


def get_user_tweets(user: User) -> List[Tweet]:
    """
    Retrieve a list of tweets created by the given user.

    Args:
        user (User): The user whose tweets are to be retrieved.

    Returns:
        List[Tweet]: List of tweets by the user.
    """

    return list(Tweet.objects.filter(user=user).order_by("-created_at"))


def get_tweet_and_replies(tweet_id: int) -> Tuple[Tweet, List[Tweet]]:
    """
    Retrieve a tweet and its replies based on the tweet ID.

    Args:
        tweet_id (int): The ID of the tweet.

    Returns:
        Tuple[Tweet, List[Tweet]]: A tuple containing the tweet and its list of replies.
    """

    try:
        tweet = Tweet.objects.get(pk=tweet_id)
    except Tweet.DoesNotExist as err:
        logger.error("Tweet not found.", extra={"tweet_id": tweet_id}, exc_info=err)
        raise TweetNotFound

    replies = list(Tweet.objects.filter(reply_to=tweet).order_by("created_at"))
    return tweet, replies


def get_tweets_from_following_users(user: User) -> List[Tweet]:
    """
    Retrieve tweets from users followed by the given user.

    Args:
        user (User): The user whose followed users' tweets are to be retrieved.

    Returns:
        List[Tweet]: List of tweets from followed users.
    """

    following_users = user.followers.all()
    return list(Tweet.objects.filter(user__in=following_users).order_by("-created_at"))


def get_reposts_from_following_users(user: User) -> List[Tweet]:
    """
    Retrieve reposted tweets from users followed by the given user.

    Args:
        user (User): The user whose followed users' reposted tweets are to be retrieved.

    Returns:
        List[Tweet]: List of reposted tweets from followed users.
    """

    following_users = user.followers.all()
    return list(Tweet.objects.filter(repost__user__in=following_users).order_by("-created_at"))


def like_tweet(user: User, tweet: Tweet) -> None:
    """
    Like a tweet.

    Args:
        user (User): The user performing the action.
        tweet (Tweet): The tweet to be liked.

    Raises:
        UnauthorizedAction: If the user tries to like their own tweet.

    Returns:
        None
    """

    if tweet.user == user:
        raise UnauthorizedAction("Cannot like own tweet")
    tweet.like.add(user)


def repost_tweet(user: User, tweet: Tweet) -> None:
    """
    Repost a tweet.

    Args:
        user (User): The user performing the action.
        tweet (Tweet): The tweet to be reposted.
    Raises:
        UnauthorizedAction: If the user tries to repost their own tweet.

    Returns:
        None
    """

    if tweet.user == user:
        raise UnauthorizedAction("Cannot repost own tweet")
    tweet.repost.add(user)
