import logging

from core.business_logic.errors import UnauthorizedAction
from core.models import Notification, NotificationType, Tweet, User

from .notifications import create_message

logger = logging.getLogger(__name__)


def repost_tweet(user: User, tweet_id: int) -> None:
    """
    Repost a tweet. Create notification about repost.

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
        notification_type = NotificationType.objects.get(name="repost")
        message = create_message(user=user, tweet=tweet, notification_type=notification_type)
        notification = Notification.objects.create(message=message, notification_type=notification_type)
        notification.user.add(tweet.user)
        logger.info(
            msg="Notification about repost has been created", extra={"to_user": tweet.user_id, "tweet": tweet.pk}
        )
    else:
        tweet.repost.remove(user)
        logger.info(f"User '{user.username}' remove repost on tweet with ID {tweet.pk}.")
