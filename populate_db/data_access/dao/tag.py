from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from data_access.settings import LOGGING

from .base import BaseDAO

if TYPE_CHECKING:
    from dto import TagDTO


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class TagDAO(BaseDAO):
    """Contains methods for working with the "tags" table from the database."""

    def create(self, data: TagDTO) -> None:
        """Executes data writing to a PostgreSQL table."""

        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO tags (name, created_at, updated_at) VALUES (%s, %s, %s);",
                (data.name, data.created_at, data.updated_at),
            )
        except Exception as exc:
            self._db_gateway.connection.rollback()
            logging.error("DB error. Error info: ", exc_info=exc)
            raise Exception from exc
        else:
            self._db_gateway.connection.commit()

    def get_ids_list(self) -> list[int]:
        """Gets ids from PostgreSQL table."""

        self._db_gateway.cursor.execute("SELECT id FROM tags;")
        final_result: list[int] = self._db_gateway.cursor.fetchall()
        return final_result
