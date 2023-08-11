from __future__ import annotations

from core.business_logic.errors import InvalidAuthCredentialsError
from django.contrib.auth import authenticate
from typing import TYPE_CHECKING
from core.models import User
import logging
if TYPE_CHECKING:
    from core.business_logic.dto import SignInDTO


logger = logging.getLogger(__name__)

def authenticate_user(data: SignInDTO) -> ...:
    logger.info("Start authentication")
    user = authenticate(username=data.email, password=data.password)
    if user is not None:
        return user
    else:
        raise InvalidAuthCredentialsError
