from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.settings import LOGGING

from .base import BaseDAO

if TYPE_CHECKING:
    from core.management.populate_db_script.data_access.dto import NotificationDTO


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class NotificationDAO(BaseDAO):
    """Contains methods for working with the "notifications" table from the database."""

    def create(self, data: NotificationDTO) -> None:
        """Executes data writing to a PostgreSQL table."""

        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO notifications (message, notification_type_id, created_at, updated_at) VALUES"
                " (%s, %s, %s, %s);",
                (data.message, data.notification_type_id, data.created_at, data.updated_at),
            )
            self._db_gateway.cursor.execute(
                "INSERT INTO notifications_users (user_id, notification_id) VALUES" " (%s, %s);",
                (data.user.user_id, data.user.notification_id),
            )
        except Exception as exc:
            self._db_gateway.connection.rollback()
            logging.error("DB error. Error info: ", exc_info=exc)
            raise Exception from exc
        else:
            self._db_gateway.connection.commit()

    def get_notification_type_id_list(self) -> list[tuple[int,]]:
        """Gets ids from PostgreSQL table."""
        self._db_gateway.cursor.execute("SELECT id FROM notification_types;")
        final_result: list[tuple[int,]] = self._db_gateway.cursor.fetchall()
        return final_result

    def get_notification_ids_list(self) -> list[tuple[int,]]:
        """Gets ids from PostgreSQL table."""
        self._db_gateway.cursor.execute("SELECT id FROM notifications;")
        final_result: list[tuple[int,]] = self._db_gateway.cursor.fetchall()
        return final_result
