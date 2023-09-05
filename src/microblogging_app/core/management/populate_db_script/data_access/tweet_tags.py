from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from .base import BaseDAO

logger = getLogger(__name__)

if TYPE_CHECKING:
    from core.models import Tweet


class TweetTagsDAO(BaseDAO):
    def get_objects_list(self) -> list[Tweet.tags.through]:
        """Gets ids from PostgreSQL table."""

        ids_list: list[Tweet.tags.through] = list(self._db_model.objects.select_related("tag", "tweet").all())
        return ids_list
