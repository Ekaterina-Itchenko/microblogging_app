from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.models import Notification, Tweet, User
from django.conf import settings

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from core.models import NotificationType
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


@query_debugger
def get_user_notifications(user: User) -> QuerySet:
    notifications = (
        Notification.objects.filter(user_id=user.pk).select_related("notification_type").order_by("-created_at")
    )
    return notifications


@query_debugger
def create_message(user: User, tweet: Tweet, notification_type: NotificationType) -> str:
    tweet_url = settings.SERVER_HOST + f"/tweet/{tweet.id}"
    user_url = settings.SERVER_HOST + f"/{user.username}/profile/"
    if notification_type.name == "like":
        message = f"User {user_url} has liked your tweet {tweet_url}"
    else:
        message = f"User {user_url} has reposted your tweet {tweet_url}"
    return message
