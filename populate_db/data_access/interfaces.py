from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from psycopg2 import connection, cursor  # noqa: F401


class DBGatewayProtocol(Protocol):
    """Describes interface of object that creates cursor and connection objects for working with the database."""

    cursor: cursor
    connection: connection


class CreateRecordProtocol(Protocol):
    """Describes interface of object that creates record to the database."""

    def create(self, data: object) -> None:
        """Executes data writing to a database table."""

        raise NotImplementedError


class GetIdsListProtocol(Protocol):
    """Describes interface of object that gets data about ids from the database."""

    def get_ids_list(self) -> list[int]:
        """Gets ids from database table."""

        raise NotImplementedError
