from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from data_access.settings import LOGGING

from .base import BaseDAO

if TYPE_CHECKING:
    from dto import UserDTO


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class UserDAO(BaseDAO):
    """Contains methods for working with the "users" table from the database."""

    def create(self, data: UserDTO) -> None:
        """Executes data writing to a PostgreSQL table."""

        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO users (username, first_name, last_name, is_active, description, birth_date, email, "
                "country_id, password, created_at, updated_at, is_superuser, is_staff, date_joined) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                (
                    data.username,
                    data.first_name,
                    data.last_name,
                    data.is_active,
                    data.description,
                    data.birth_date,
                    data.email,
                    data.country_id,
                    data.encrypted_password,
                    data.created_at,
                    data.updated_at,
                    data.is_superuser,
                    data.is_staff,
                    data.created_at,
                ),
            )
        except Exception as exc:
            self._db_gateway.connection.rollback()
            logging.error("DB error. Error info: ", exc_info=exc)
            raise Exception from exc
        else:
            self._db_gateway.connection.commit()

    def get_ids_list(self) -> list[tuple[int,]]:
        """Gets ids from PostgreSQL table."""

        self._db_gateway.cursor.execute("SELECT id FROM users;")
        final_result: list[tuple[int,]] = self._db_gateway.cursor.fetchall()
        return final_result
