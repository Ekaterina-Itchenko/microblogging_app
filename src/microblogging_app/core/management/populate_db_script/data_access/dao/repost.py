from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.settings import LOGGING

from .base import BaseDAO

if TYPE_CHECKING:
    from core.management.populate_db_script.data_access.dto import RepostDTO


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class RepostDAO(BaseDAO):
    """Contains methods for working with the "countries" table from the database."""

    def create(self, data: RepostDTO) -> None:
        """Executes data writing to a PostgreSQL table."""

        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO reposts (tweet_id, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s);",
                (data.tweet_id, data.user_id, data.created_at, data.updated_at),
            )
        except Exception as exc:
            self._db_gateway.connection.rollback()
            logging.error("DB error. Error info: ", exc_info=exc)
            raise Exception from exc
        else:
            self._db_gateway.connection.commit()
