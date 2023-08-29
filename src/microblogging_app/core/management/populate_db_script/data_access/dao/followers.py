from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.settings import LOGGING

from .base import BaseDAO

if TYPE_CHECKING:
    from core.management.populate_db_script.data_access.dto import FollowersDTO


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class FollowersDAO(BaseDAO):
    """Contains methods for working with the "followers" table from the database."""

    def create(self, data: FollowersDTO) -> None:
        """Executes data writing to a PostgreSQL table."""
        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO followers (from_user_id, to_user_id) VALUES (%s, %s);",
                (data.from_user_id, data.to_user_id),
            )
        except Exception as exc:
            self._db_gateway.connection.rollback()
            logging.error("DB error. Error info: ", exc_info=exc)
            raise Exception from exc
        else:
            self._db_gateway.connection.commit()
