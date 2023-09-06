"""
Custom migration that populate NotificationType table with default values.
"""

from typing import Any

from core.models import NotificationType
from django.db import migrations

DEFAULT_VALUES = ("admin", "like", "repost", "reply")


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""
    types_list = [NotificationType(name=not_type) for not_type in DEFAULT_VALUES]
    NotificationType.objects.bulk_create(types_list, ignore_conflicts=True)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    NotificationType.objects.raw("TRUNCATE TABLE notification_types")


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("core", "0002_populate_countries_table"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
