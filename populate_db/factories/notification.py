from __future__ import annotations

from typing import TYPE_CHECKING

from data_access.dto import NotificationDTO

if TYPE_CHECKING:
    from providers import NotificationMessageProvider, RandomValueFromListProvider


class NotificationFactory:
    """Contains methods for generating values for NotificationDTO."""

    def __init__(
        self,
        notification_message_provider: NotificationMessageProvider,
        random_user_provider: RandomValueFromListProvider,
        random_note_type_provider: RandomValueFromListProvider,
    ):
        self._random_user_provider = random_user_provider
        self._notification_message_provider = notification_message_provider
        self._random_note_type_provider = random_note_type_provider

    def generate(self) -> NotificationDTO:
        """Generates random data for NotificationDTO"""

        notification_id = self._random_note_type_provider()
        return NotificationDTO(
            user_id=self._random_user_provider(),
            notification_type_id=notification_id,
            message=self._notification_message_provider(random_note_type_id=notification_id),
        )
