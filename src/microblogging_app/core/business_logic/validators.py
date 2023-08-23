from __future__ import annotations

import logging

from core.business_logic.errors import UnauthorizedAction
from core.models import Tweet, User

logger = logging.getLogger(__name__)


def validate_tweet_owner(user: User, tweet: Tweet) -> None:
    if tweet.user_id == user.pk:
        logger.error(
            msg="Cannot like or repost an own tweet",
            extra={"user": user.pk, "tweet_id": tweet},
        )
        raise UnauthorizedAction
    else:
        return None
