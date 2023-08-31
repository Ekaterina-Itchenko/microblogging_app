from __future__ import annotations

from typing import TYPE_CHECKING

from core.management.populate_db_script.data_access.dto import (
    NotificationDTO,
    NotificationUserDTO,
)

if TYPE_CHECKING:
    from core.management.populate_db_script.providers import (
        NotificationMessageProvider,
        RandomValueFromListProvider,
    )


class NotificationFactory:
    """Contains methods for generating values for NotificationDTO."""

    def __init__(
        self,
        notification_message_provider: NotificationMessageProvider,
        random_user_provider: RandomValueFromListProvider,
        random_notification_id_provider: RandomValueFromListProvider,
        random_note_type_provider: RandomValueFromListProvider,
    ):
        self._random_user_provider = random_user_provider
        self._notification_message_provider = notification_message_provider
        self._random_note_type_provider = random_note_type_provider
        self._random_notification_id_provider = random_notification_id_provider

    def generate(self) -> NotificationDTO:
        """Generates random data for NotificationDTO"""

        return NotificationDTO(
            user=NotificationUserDTO(
                user_id=self._random_user_provider(), notification_id=self._random_notification_id_provider()
            ),
            notification_type_id=self._random_note_type_provider(),
            message=self._notification_message_provider(),
        )
