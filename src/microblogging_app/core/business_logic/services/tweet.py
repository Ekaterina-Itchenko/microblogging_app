import logging
import re
from typing import Any

from core.business_logic.dto import AddTweetDTO, EditTweetDTO
from core.business_logic.errors import TweetNotFound
from core.models import Tag, Tweet
from django.db import transaction
from django.db.models import Count

from microblogging_app.utils import query_debugger

logger = logging.getLogger(__name__)


@query_debugger
def create_tweet(data: AddTweetDTO) -> Any:
    """
    Create a new tweet.
    Args:
        data (AddTweetData): Data containing tweet information.
    Returns:
        None
    """

    with transaction.atomic():
        if data.reply_to_id:
            try:
                tweet_reply_to = Tweet.objects.get(pk=data.reply_to_id)
            except Tweet.DoesNotExist:
                logger.error("The tweet you want to reply doesn't exist.", extra={"tweet_reply_to": data.reply_to_id})
                raise TweetNotFound
        else:
            tweet_reply_to = None

        created_tweet = Tweet.objects.create(user=data.user, content=data.content, reply_to=tweet_reply_to)
        if data.tags != "":
            tags: list[str] = re.split("[ \r\n]+", data.tags)
            tags_list: list[Tag] = []
            for tag in tags:
                try:
                    tag_from_db = Tag.objects.get(name=tag.lower())
                except Tag.DoesNotExist as err:
                    logger.warning("Tag doesn't exist.", extra={"Tag": tag}, exc_info=err)
                    tag_from_db = Tag.objects.create(name=tag.lower())
                    logger.info("Handled error and successfully created tag in db.", extra={"tag": tag})
                tags_list.append(tag_from_db)
            created_tweet.tags.set(tags_list)
        logger.info(
            "Successfully created tweet",
            extra={
                "user": (data.user.username if data.user is not None else None),
                "content": data.content,
                "reply_to": data.reply_to_id,
            },
        )
    return created_tweet.pk


def get_tweet_info(tweet_id: int) -> Tweet:
    """
    Retrieve a tweet based on the tweet ID.
    Args:
        tweet_id (int): The ID of the tweet.
    Returns:
        tweet (Tweet): A tweet received by its id.
    """

    try:
        tweet: Tweet = (
            Tweet.objects.annotate(
                num_reposts=Count("reposts", distinct=True),
                num_likes=Count("likes", distinct=True),
                num_replies=Count("tweets_replies", distinct=True),
            )
            .prefetch_related("like", "repost", "tags")
            .select_related("user", "reply_to", "reply_to__user")
            .get(pk=tweet_id)
        )
        return tweet
    except Tweet.DoesNotExist as err:
        logger.error("Tweet not found.", extra={"tweet_id": tweet_id}, exc_info=err)
        raise TweetNotFound


@query_debugger
def edit_tweet(data: EditTweetDTO) -> Any:
    """
    Edit tweet in the DB.
    Args:
        data (EditTweetData): Data containing tweet information.
    Returns:
        tweet_id or None
    """
    with transaction.atomic():
        edited_tweet: Tweet = Tweet.objects.prefetch_related("tags").get(pk=data.tweet_id)
        if data.tags != "":
            tags: list[str] = re.split("[ \r\n]+", data.tags)
            tags_list: list[Tag] = []
            for tag in tags:
                try:
                    tag_from_db = Tag.objects.get(name=tag.lower())
                except Tag.DoesNotExist as err:
                    logger.warning("Tag doesn't exist.", extra={"Tag": tag}, exc_info=err)
                    tag_from_db = Tag.objects.create(name=tag.lower())
                    logger.info("Handled error and successfully created tag in db.", extra={"tag": tag})
                tags_list.append(tag_from_db)
            edited_tweet.tags.set(tags_list)
        else:
            for tag in edited_tweet.tags.all():
                edited_tweet.tags.remove(tag)
        edited_tweet.content = data.content
        edited_tweet.save()
        logger.info("Successfully updated tweet", extra={"tweet_id": data.tweet_id, "content": data.content})
    return edited_tweet.pk
