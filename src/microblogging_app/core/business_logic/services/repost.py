import logging

from core.business_logic.errors import UnauthorizedAction
from core.models import Tweet, User

logger = logging.getLogger(__name__)


def repost_tweet(user: User, tweet_id: int) -> None:
    """
    Repost a tweet.

    Args:
        user (User): The user performing the action.
        tweet_id (int): The ID of tweet to be reposted.
    Raises:
        UnauthorizedAction: If the user tries to repost their own tweet.

    Returns:
        None
    """
    tweet = Tweet.objects.select_related("user").prefetch_related("repost").get(pk=tweet_id)
    if tweet.user == user:
        raise UnauthorizedAction("Cannot repost own tweet")
    if user not in tweet.repost.all():
        tweet.repost.add(user)
        logger.info(f"User '{user.username}' repost tweet with ID {tweet.pk}.")
    else:
        tweet.repost.remove(user)
        logger.info(f"User '{user.username}' remove repost on tweet with ID {tweet.pk}.")
