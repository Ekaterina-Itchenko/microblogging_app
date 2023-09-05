from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from .base import BaseDAO

logger = getLogger(__name__)

if TYPE_CHECKING:
    from core.models import User


class FollowersDAO(BaseDAO):
    def get_objects_list(self) -> list[User.following.through]:
        """Gets ids from PostgreSQL table."""

        ids_list: list[User.following.through] = list(
            self._db_model.objects.select_related("from_user", "to_user").all()
        )
        return ids_list
