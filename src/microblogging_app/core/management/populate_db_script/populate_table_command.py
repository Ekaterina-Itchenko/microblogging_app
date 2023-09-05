from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.management.populate_db_script.data_access import BaseDAO
    from core.management.populate_db_script.factories.interfaces import (
        FakeFactoryProtocol,
    )


class PopulateTable:
    """Contains methods and logic for writing data to the database."""

    def __init__(self, records_number: int, dao: BaseDAO, fake_factory: FakeFactoryProtocol) -> None:
        self._records_number = records_number
        self._dao = dao
        self._fake_factory = fake_factory

    def execute(self) -> None:
        """Executes a data recording into the database."""

        for _ in range(self._records_number):
            new_record = self._fake_factory.generate()
            self._dao.append_model_to_list(model=new_record)
        self._dao.create_record()
