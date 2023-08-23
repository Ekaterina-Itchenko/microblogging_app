from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from core.business_logic.dto.home import TweetDTO
from core.business_logic.errors import (
    TweetAlreadyLikedByUserError,
    TweetAlreadyRepostedByUserError,
    TweetNotFound,
)
from core.business_logic.validators import validate_tweet_owner
from core.models import Like, Repost, Tag, Tweet, User
from django.db import IntegrityError, transaction
from django.db.models import Count, Q

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.db.models import QuerySet

logger = logging.getLogger(__name__)


@query_debugger
def create_tweet(data: TweetDTO, user: User, reply_to: Optional[int] = None) -> None:
    """
    Create a new tweet or reply of a tweet and update reply count if it's a reply.
    Args:
        data (TweetData): Data containing tweet information.
        user (User): The user who create this tweet.
        reply_to (Tweet | None): When created tweet is a reply to another tweet.
    Returns:
        None
    """
    try:
        with transaction.atomic():
            tags = [tag.lower() for tag in data.tags.split("\r\n")]
            related_tags = []
            for tag in tags:
                try:
                    received_tag = Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    received_tag = Tag.objects.create(name=tag)
                related_tags.append(received_tag)
            if reply_to:
                tweet_reply_to = Tweet.objects.get(pk=reply_to)
                tweet_reply_to.reply_counter += 1
                tweet_reply_to.save()

            created_tweet = Tweet.objects.create(
                user=user,
                content=data.content,
                reply_to=reply_to,
            )
            created_tweet.tags.set(related_tags)

            logger.info("Tweet has been created", extra={"user": user.pk, "reply_to": reply_to})
    except Tweet.DoesNotExist:
        logger.error("The tweet you want to reply to doesn't exist.", extra={"tweet_reply_to": reply_to})
        raise TweetNotFound


@query_debugger
def get_tweet(tweet_id: int) -> Tweet:
    """
    Retrieve a tweet based on the tweet ID.
    Args:
        tweet_id (int): The ID of the tweet.
    Returns:
        tweet (Tweet): A tweet received by its id.
    """

    try:
        tweet = (
            Tweet.objects.annotate(num_likes=Count("likes", distinct=True), num_reposts=Count("reposts", distinct=True))
            .select_related("user")
            .get(pk=tweet_id)
        )
    except Tweet.DoesNotExist as err:
        logger.error("Tweet not found.", extra={"tweet_id": tweet_id}, exc_info=err)
        raise TweetNotFound
    return tweet


@query_debugger
def get_replies(tweet_id: int) -> QuerySet:
    """
    Retrieve tweets replies based on the tweet ID.
    Args:
        tweet_id (int): The ID of the tweet.
    Returns:
        QuerySet: A queryset containing the tweets replies.
    """

    replies = Tweet.objects.filter(reply_to=tweet_id).select_related("user").order_by("created_at")
    return replies


@query_debugger
def get_tweets_reposts_from_following_users(user: User) -> QuerySet:
    """
    Retrieve tweets from users followed by the given user.
    Args:
        user (User): The user whose followed users' tweets are to be retrieved.
    Returns:
        QuerySet of tweets from following users.
    """

    following_users = user.followers.all()

    result = (
        Tweet.objects.annotate(num_likes=Count("likes", distinct=True), num_reposts=Count("reposts", distinct=True))
        .filter(Q(user__in=following_users) | Q(reposts__user__in=following_users))
        .select_related("user")
        .values(
            "id",
            "content",
            "user__username",
            "user__first_name",
            "user__last_name",
            "created_at",
            "reply_counter",
            "num_likes",
            "num_reposts",
        )
    )

    return result


@query_debugger
def ordering_tweets(tweets: QuerySet, condition: str) -> QuerySet:
    """
    Order tweets by received condition.
    Args:
       tweets (QuerySet): The user whose followed users' tweets are to be retrieved.
       condition: Condition for ordering
    Returns:
        Ordered QuerySet of tweets.
    """

    if condition == "most_likes":
        most_likes_tweets = tweets.order_by("-num_likes")
        return most_likes_tweets
    else:
        newest_tweets = tweets.order_by("-created_at")
        return newest_tweets


@query_debugger
def like_tweet(user: User, tweet_id: int) -> None:
    """
    Like a tweet.
    Args:
        user (User): The user performing the action.
        tweet_id (int): The id of the tweet to be liked.
    """
    try:
        tweet = Tweet.objects.get(pk=tweet_id)
        validate_tweet_owner(user=user, tweet=tweet)
        Like.objects.create(user=user, tweet=tweet)
    except Tweet.DoesNotExist:
        logger.error(
            msg="Such tweet does not exist.",
            extra={"user": user.pk, "tweet_id": tweet_id},
        )
        raise TweetNotFound
    except IntegrityError:
        logger.error(
            msg="User has already liked this tweet.",
            extra={"user": user.pk, "tweet_id": tweet_id},
        )
        raise TweetAlreadyLikedByUserError


@query_debugger
def repost_tweet(user: User, tweet_id: int) -> None:
    """
    Repost a tweet.
    Args:
        user (User): The user performing the action.
        tweet_id (int): The id of the tweet to be reposted.
    """
    try:
        tweet = Tweet.objects.get(pk=tweet_id)
        validate_tweet_owner(user=user, tweet=tweet)
        Repost.objects.create(user=user, tweet=tweet)
    except Tweet.DoesNotExist:
        logger.error(
            msg="Such tweet does not exist.",
            extra={"user": user.pk, "tweet_id": tweet_id},
        )
        raise TweetNotFound
    except IntegrityError:
        logger.error(
            msg="User has already reposted this tweet.",
            extra={"user": user.pk, "tweet_id": tweet_id},
        )
        raise TweetAlreadyRepostedByUserError
