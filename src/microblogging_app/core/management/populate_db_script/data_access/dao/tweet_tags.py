from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.settings import LOGGING

from .base import BaseDAO

if TYPE_CHECKING:
    from core.management.populate_db_script.data_access.dto import TweetTagsDTO


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class TweetTagsDAO(BaseDAO):
    """Contains methods for working with the "tweet_tags" table from the database."""

    def create(self, data: TweetTagsDTO) -> None:
        """Executes data writing to a PostgreSQL table."""

        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO tweet_tags (tweet_id, tag_id) VALUES (%s, %s);", (data.tweet_id, data.tag_id)
            )
        except Exception as exc:
            self._db_gateway.connection.rollback()
            logging.error("DB error. Error info: ", exc_info=exc)
            raise Exception from exc
        else:
            self._db_gateway.connection.commit()
