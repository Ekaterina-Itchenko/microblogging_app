from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING
from uuid import uuid4

from core.business_logic.errors import (
    ConfirmationCodeDoesNotExistError,
    ConfirmationCodeExpiredError,
    UserAlreadyExistsError,
)
from core.models import EmailConfirmationCodes
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.urls import reverse

if TYPE_CHECKING:
    from core.business_logic.dto import RegistrationDTO
    from core.models import User


logger = logging.getLogger(__name__)


def create_user(received_data: RegistrationDTO) -> None:
    """Records registration data to the database table User."""

    user = get_user_model()
    try:
        created_user = user.objects.create_user(
            email=received_data.email,
            username=received_data.username,
            birth_date=received_data.birth_date,
            password=received_data.password,
            is_active=False,
        )
        logger.info(msg="Created user.", extra={"user_email": received_data.email})
    except IntegrityError:
        logger.info(
            msg="Such email or username already exist.",
            extra={"user_email": received_data.email, "username": received_data.username},
        )
        raise UserAlreadyExistsError

    send_confirmation_email(user=created_user)


def send_confirmation_email(user: User) -> None:
    """
    Send email to confirm a registration.
    Confirmation code is sent as a query parameter in a link.
    """

    confirmation_code = str(uuid4())
    expiration_time = settings.CONFIRMATION_CODE_EXPIRATION_TIME + int(time.time())

    EmailConfirmationCodes.objects.create(code=confirmation_code, user=user, expiration=expiration_time)
    confirmation_url = settings.SERVER_HOST + reverse("sign_up_confirmation") + f"?code={confirmation_code}"
    send_mail(
        subject="Confirm your email.",
        message=f"Please confirm your email by clicking the link below:\n\n{confirmation_url}",
        from_email=settings.EMAIL_FROM,
        recipient_list=[user.email],
    )
    logger.info(msg="Confirmation link has been sent.", extra={"user": user.email, "code": confirmation_code})
    return None


def confirm_user_registration(confirmation_code: str) -> None:
    """
    Check the received confirmation code in query parameters with confirmation code in the database.
    Check the expiration time of the confirmation code. If the expiration time is expired, a new email
    with a new confirmation code will send.
    """

    try:
        email_confirmation_object = EmailConfirmationCodes.objects.get(code=confirmation_code)
    except EmailConfirmationCodes.DoesNotExist:
        logger.error("An invalid confirmation code has been received.")
        raise ConfirmationCodeDoesNotExistError

    user = email_confirmation_object.user
    current_time = time.time()
    if current_time > email_confirmation_object.expiration:
        email_confirmation_object.delete()
        logger.info(
            msg="The confirmation code has been removed because expiration time is up.",
            extra={"Current time": current_time, "Expiration time": email_confirmation_object.expiration},
        )

        send_confirmation_email(user=user)
        logger.info(
            msg="The new confirmation code has been sent",
            extra={"new_code": EmailConfirmationCodes.objects.get(user=user), "user": user},
        )

        raise ConfirmationCodeExpiredError

    user.is_active = True
    logger.info(msg="The user is activated.", extra={"user": user.email})

    user.save()
    email_confirmation_object.delete()
    logger.info(msg="The confirmation code has been removed because the user is activated.", extra={"user": user.email})
