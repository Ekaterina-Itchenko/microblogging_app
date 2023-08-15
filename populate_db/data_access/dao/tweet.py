from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from data_access.settings import LOGGING

from .base import BaseDAO

if TYPE_CHECKING:
    from dto import TweetDTO


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class TweetDAO(BaseDAO):
    """Contains methods for working with the "tweets" table from the database."""

    def create(self, data: TweetDTO) -> None:
        """Executes data writing to a PostgreSQL table."""

        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO tweets (content, reply_to_id, user_id, created_at, updated_at, reply_counter) VALUES "
                "(%s, %s, %s, %s, %s, %s);",
                (data.content, data.reply_to, data.user_id, data.created_at, data.updated_at, data.reply_counter),
            )
        except Exception as exc:
            self._db_gateway.connection.rollback()
            logging.error("DB error. Error info: ", exc_info=exc)
            raise Exception from exc
        else:
            self._db_gateway.connection.commit()
        if data.reply_to is not None:
            self._db_gateway.cursor.execute("SELECT reply_counter FROM tweets WHERE id = (%s)", (data.reply_to,))
            tuple_res = self._db_gateway.cursor.fetchone()
            replies_counter_from_db = int(tuple_res[0])
            updated_replies_counter = replies_counter_from_db + 1
            try:
                self._db_gateway.cursor.execute(
                    "UPDATE tweets SET reply_counter = %s WHERE id = (%s)", (updated_replies_counter, data.reply_to)
                )
            except Exception as exc:
                self._db_gateway.connection.rollback()
                logging.error("DB error. Error info: ", exc_info=exc)
                raise Exception from exc
            else:
                self._db_gateway.connection.commit()

    def get_ids_list(self) -> list[tuple[int,]]:
        """Gets ids from PostgreSQL table."""

        self._db_gateway.cursor.execute("SELECT id FROM tweets;")
        final_result: list[tuple[int,]] = self._db_gateway.cursor.fetchall()
        return final_result
