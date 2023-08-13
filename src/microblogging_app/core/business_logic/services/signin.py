from __future__ import annotations

from core.business_logic.errors import InvalidAuthCredentialsError
from django.contrib.auth import authenticate

import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.business_logic.dto import SignInDTO
    from django.contrib.auth.models import AbstractUser


logger = logging.getLogger(__name__)


def authenticate_user(data: SignInDTO) -> AbstractUser:
    """Authentication of user"""

    user = authenticate(email=data.email, password=data.password)
    if user is not None:
        return user
    else:
        logger.error(
            msg="Invalid an email or a password.",
            extra={"user": data.email, "password": data.password}
        )
        raise InvalidAuthCredentialsError
