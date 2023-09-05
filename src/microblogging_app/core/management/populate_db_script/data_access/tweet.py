from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from .base import BaseDAO

logger = getLogger(__name__)

if TYPE_CHECKING:
    from core.models import Tweet


class TweetDAO(BaseDAO):
    def get_objects_list(self) -> list[Tweet]:
        """Gets ids from PostgreSQL table."""

        ids_list: list[Tweet] = list(self._db_model.objects.select_related("user", "reply_to").all())
        return ids_list
