from __future__ import annotations

from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.dto import TagDTO

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import RandomTagProvider


class TagFactory:
    """Contains methods for generating values for TagDTO."""

    def __init__(self, random_tag_provider: RandomTagProvider):
        self._random_tag_provider = random_tag_provider

    def generate(self) -> TagDTO:
        """Generates random data for TagDTO"""

        return TagDTO(name=self._random_tag_provider())
