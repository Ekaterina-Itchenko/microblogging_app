from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from data_access.settings import LOGGING

from .base import BaseDAO

if TYPE_CHECKING:
    from dto import LikeDTO


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class LikeDAO(BaseDAO):
    """Contains methods for working with the "likes" table from the database."""

    def create(self, data: LikeDTO) -> None:
        """Executes data writing to a PostgreSQL table."""

        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO likes (tweet_id, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s);",
                (data.tweet_id, data.user_id, data.created_at, data.updated_at),
            )
        except Exception as exc:
            self._db_gateway.connection.rollback()
            logging.error("DB error. Error info: ", exc_info=exc)
            raise Exception from exc
        else:
            self._db_gateway.connection.commit()
