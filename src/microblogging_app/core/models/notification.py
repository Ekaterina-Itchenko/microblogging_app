"""
"Core" app Notification model of microblogging_app project.
"""

from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models


class Notification(BaseModel):
    """Describes the fields and attributes of the Notification model in the database."""

    message = models.CharField(max_length=400, null=False)
    user = models.ManyToManyField(to=get_user_model(), related_name="notifications", db_table="notifications_users")
    notification_type = models.ForeignKey(to="NotificationType", on_delete=models.CASCADE, related_name="notifications")

    class Meta:
        """Describes class metadata."""

        db_table = "notifications"


class NotificationType(BaseModel):
    """Describes the fields and attributes of the Notification model in the database."""

    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        """Describes class metadata."""

        db_table = "notification_types"
