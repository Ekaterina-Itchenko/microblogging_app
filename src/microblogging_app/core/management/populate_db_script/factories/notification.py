from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import Notification, NotificationType

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        NotificationMessageProvider,
        RandomObjectFromListProvider,
    )


class NotificationFactory:
    """Contains methods for generating values for Notification model."""

    def __init__(
        self,
        notification_message_provider: NotificationMessageProvider,
        admin_notification_type_object: NotificationType,
    ):
        self._notification_message_provider = notification_message_provider
        self._admin_notification_type_object = admin_notification_type_object

    def generate(self) -> Notification:
        """Generates random data for NotificationDTO"""

        return Notification(
            message=self._notification_message_provider(), notification_type=self._admin_notification_type_object
        )


class NotificationUserFactory:
    """Contains methods for generating values for Notification model."""

    def __init__(
        self,
        random_notification_provider: RandomObjectFromListProvider,
        random_user_provider: RandomObjectFromListProvider,
    ):
        self._random_notification_provider = random_notification_provider
        self._random_user_provider = random_user_provider

    def generate(self) -> Notification:
        """Generates random data for NotificationDTO"""

        return Notification.user.through(
            notification=self._random_notification_provider(), user=self._random_user_provider()
        )
