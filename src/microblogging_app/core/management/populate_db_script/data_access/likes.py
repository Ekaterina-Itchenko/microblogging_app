from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from .base import BaseDAO

logger = getLogger(__name__)

if TYPE_CHECKING:
    from core.models import Like


class LikesDAO(BaseDAO):
    def get_objects_list(self) -> list[Like]:
        """Gets ids from PostgreSQL table."""

        ids_list: list[Like] = list(self._db_model.objects.select_related("tweet", "user").all())
        return ids_list
