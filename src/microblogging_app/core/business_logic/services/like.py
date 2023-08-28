import logging

from core.business_logic.errors import TweetNotFound, UnauthorizedAction
from core.models import Notification, NotificationType, Tweet, User

from microblogging_app.utils import query_debugger

from .notifications import create_message

logger = logging.getLogger(__name__)


@query_debugger
def like_tweet(user: User, tweet_id: int) -> None:
    """
    Like and unlike a tweet. Create notification about like.

    Args:
        user (User): The user performing the action.
        tweet_id (int): The ID of tweet to be liked.

    Raises:
        UnauthorizedAction: If the user tries to like their own tweet.

    Returns:
        None
    """
    try:
        tweet = Tweet.objects.prefetch_related("like").get(pk=tweet_id)
    except Tweet.DoesNotExist:
        logger.error(
            msg="Such tweet does not exist.",
            extra={"user": user.pk, "tweet_id": tweet_id},
        )
        raise TweetNotFound
    if tweet.user_id == user.pk:
        raise UnauthorizedAction("Cannot like own tweet")
    if user not in tweet.like.all():
        tweet.like.add(user)
        logger.info(f"User '{user.username}' liked tweet with ID {tweet.pk}.")
        notification_type = NotificationType.objects.get(name="like")
        message = create_message(user=user, tweet=tweet, notification_type=notification_type)
        notification = Notification.objects.create(message=message, notification_type=notification_type)
        notification.user.add(tweet.user)
        logger.info(msg="Notification about like has been created", extra={"to_user": tweet.user_id, "tweet": tweet.pk})
    else:
        tweet.like.remove(user)
        logger.info(f"User '{user.username}' remove like from tweet with ID {tweet.pk}.")
