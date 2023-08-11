
from __future__ import annotations
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


import logging


logger = logging.getLogger(__name__)


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email: str = None, password: str = None) -> AbstractUser:
        user_model = get_user_model()
        logger.info(f"APPLIED user model: {user_model.__call__}")
        try:
            user = user_model.objects.get(email=email)
            logger.info(f"user: {user.password}")
        except user_model.DoesNotExist:
            print("Нет модели")
            return None

        if not user_model.check_password(password):
            return None

        return user
 
    def get_user(self, request, user_id: int) -> AbstractUser:
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
