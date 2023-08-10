"""
Models package attributes.
"""

from .base import BaseModel

# The custom User model that is used for authentication must be imported
# before other models for migrations to work correctly.
from .user import User  # isort: split

# Importing other models.
from .country import Country
from .email_confirmation_codes import EmailConfirmationCodes
from .like import Like
from .notification import Notification, NotificationType
from .repost import Repost
from .tag import Tag
from .tweet import Tweet

__all__ = [
    "BaseModel",
    "User",
    "EmailConfirmationCodes",
    "Country",
    "Notification",
    "NotificationType",
    "Tag",
    "Like",
    "Repost",
    "Tweet",
]
