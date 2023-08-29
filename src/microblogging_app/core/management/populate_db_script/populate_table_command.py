from __future__ import annotations

import logging.config
from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.settings import LOGGING

if TYPE_CHECKING:
    from core.management.populate_db_script.data_access.interfaces import (
        CreateRecordProtocol,
    )
    from core.management.populate_db_script.factories.interfaces import (
        FakeFactoryProtocol,
    )


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class PopulateTable:
    """Contains methods and logic for writing data to the database."""

    def __init__(self, records_number: int, dao: CreateRecordProtocol, fake_factory: FakeFactoryProtocol) -> None:
        self._records_number = records_number
        self._dao = dao
        self._fake_factory = fake_factory

    def execute(self) -> None:
        """Executes a data recording into the database."""
        records_num = 0
        for _ in range(self._records_number):
            new_record = self._fake_factory.generate()
            try:
                self._dao.create(data=new_record)
                records_num += 1
            except Exception:
                continue
        logger.info(
            f"Successfully added {records_num} records from {self._records_number}. "
            f"DAO: {self._dao.__module__}; FACTORY: {self._fake_factory.__module__}."
        )
