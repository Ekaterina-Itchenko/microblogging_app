from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Type

logger = getLogger(__name__)

if TYPE_CHECKING:
    from core.models import BaseModel


class BaseDAO:
    """Base Data access object."""

    def __init__(self, db_model: Type[BaseModel]) -> None:
        self._db_model = db_model
        self._models_list: list = []

    def append_model_to_list(self, model: object) -> None:
        """Appends model with generated data to models_list."""

        self._models_list.append(model)

    def create_record(self) -> None:
        """Executes data writing to a PostgreSQL table of passed model."""

        records_before = self._db_model.objects.count()
        planed_records = self._db_model.objects.bulk_create(self._models_list, ignore_conflicts=True)
        num_planed_records = len(planed_records)
        records_after = self._db_model.objects.count()
        num_added_records = records_after - records_before
        logger.info(f"Added {num_added_records} from {num_planed_records} records to {self._db_model.__name__} table.")
