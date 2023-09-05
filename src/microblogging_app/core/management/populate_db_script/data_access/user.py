from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from .base import BaseDAO

logger = getLogger(__name__)

if TYPE_CHECKING:
    from core.models import User


class UserDAO(BaseDAO):
    def get_objects_list(self) -> list[User]:
        """Gets ids from PostgreSQL table."""

        ids_list: list[User] = list(self._db_model.objects.all())
        return ids_list
