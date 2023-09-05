from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from .base import BaseDAO

logger = getLogger(__name__)

if TYPE_CHECKING:
    from core.models import Notification, NotificationType


class NotificationDAO(BaseDAO):
    def get_objects_list(self) -> list[Notification]:
        """Gets ids from PostgreSQL table."""

        ids_list: list[Notification] = list(self._db_model.objects.select_related("notification_type").all())
        return ids_list


class NotificationTypesDAO(BaseDAO):
    def get_admin_notification_type_object(self) -> NotificationType:
        """Gets NotificationType object from DB."""

        admin_notification_type_object = self._db_model.objects.get(name="admin")
        return admin_notification_type_object


class NotificationUserDAO(BaseDAO):
    def get_objects_list(self) -> list[Notification]:
        """Gets ids from PostgreSQL table."""

        ids_list: list[Notification] = list(self._db_model.objects.select_related("notification", "user").all())
        return ids_list
