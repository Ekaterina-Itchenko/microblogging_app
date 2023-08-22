from __future__ import annotations

import logging.config

from data_access.settings import LOGGING

from .base import BaseDAO

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class CountryDAO(BaseDAO):
    """Contains methods for working with the "countries" table from the database."""

    def get_ids_list(self) -> list[tuple[int,]]:
        """Gets ids from PostgreSQL table."""

        self._db_gateway.cursor.execute("SELECT id FROM countries;")
        final_result: list[tuple[int,]] = self._db_gateway.cursor.fetchall()
        return final_result
