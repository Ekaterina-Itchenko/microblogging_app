from __future__ import annotations

from core.business_logic.errors import InvalidAuthCredentialsError
from django.contrib.auth import authenticate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.business_logic.dto import SignInDTO


def authenticate_user(data: SignInDTO) -> ...:
    user = authenticate(email=data.email, password=data.password)
    if user is not None:
        return user
    else:
        raise InvalidAuthCredentialsError
