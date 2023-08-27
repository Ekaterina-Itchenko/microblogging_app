import logging

from core.business_logic.errors import TweetNotFound, UnauthorizedAction
from core.models import Tweet, User

logger = logging.getLogger(__name__)


def like_tweet(user: User, tweet_id: int) -> None:
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
    try:
        tweet = Tweet.objects.select_related("user").prefetch_related("like").get(pk=tweet_id)
    except Tweet.DoesNotExist:
        logger.error(
            msg="Such tweet does not exist.",
            extra={"user": user.pk, "tweet_id": tweet_id},
        )
        raise TweetNotFound
    if tweet.user == user:
        raise UnauthorizedAction("Cannot like own tweet")
    if user not in tweet.like.all():
        tweet.like.add(user)
        logger.info(f"User '{user.username}' liked tweet with ID {tweet.pk}.")
    else:
        tweet.like.remove(user)
        logger.info(f"User '{user.username}' remove like from tweet with ID {tweet.pk}.")
