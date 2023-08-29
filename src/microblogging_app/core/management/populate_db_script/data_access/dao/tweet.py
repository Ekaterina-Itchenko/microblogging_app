from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.settings import LOGGING

from .base import BaseDAO

if TYPE_CHECKING:
    from core.management.populate_db_script.data_access.dto import TweetDTO


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class TweetDAO(BaseDAO):
    """Contains methods for working with the "tweets" table from the database."""

    def create(self, data: TweetDTO) -> None:
        """Executes data writing to a PostgreSQL table."""

        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO tweets (content, reply_to_id, user_id, created_at, updated_at) VALUES "
                "(%s, %s, %s, %s, %s);",
                (data.content, data.reply_to, data.user_id, data.created_at, data.updated_at),
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

    def get_user_id_by_tweet_id(self, tweet_id: int) -> int:
        """Gets user_id from tweet table."""

        self._db_gateway.cursor.execute("SELECT user_id FROM tweets WHERE id = (%s);", (tweet_id,))
        tuple_res = self._db_gateway.cursor.fetchone()
        result: int = int(tuple_res[0])
        return result
