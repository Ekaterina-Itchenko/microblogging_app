from __future__ import annotations
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from core.business_logic.errors import (
    UserAlreadyExistsError,
    ConfirmationCodeDoesNotExistError,
    ConfirmationCodeExpiredError
)
from uuid import uuid4
from core.models import EmailConfirmationCodes
from django.conf import settings
import time
from django.urls import reverse
from django.core.mail import send_mail
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from core.business_logic.dto import RegistrationDTO


logger = logging.getLogger(__name__)


def create_user(received_data: RegistrationDTO) -> None:
    user = get_user_model()
    try:
        created_user = user.objects.create_user(
            email=received_data.email,
            username=received_data.username,
            birth_date=received_data.birth_date,
            password=received_data.password,
            is_active=False
        )
    except IntegrityError:
        raise UserAlreadyExistsError
    
    send_confirmation_email(user=created_user)



def send_confirmation_email(user: get_user_model) -> EmailConfirmationCodes:
    confirmation_code = str(uuid4())
    expiration_time = settings.CONRIRMATION_CODE_EXPIRATION_TIME + int(time.time())

    email_confirmation_object = EmailConfirmationCodes.objects.create(
        code=confirmation_code,
        user=user,
        expiration=expiration_time
    )
    confirmation_url = reverse("sign_up_confirmation") + f"?code={confirmation_code}"
    send_mail(
        subject="Confirm your email.",
        message=f"Please confirm your email by clicking the link below:\n\n{confirmation_url}",
        from_email=settings.EMAIL_FROM,
        recipient_list=[user.email]
    )
    logger.info(
        msg="Confirmation link has been sent.",
        extra={"user": email_confirmation_object.user, "code": email_confirmation_object.code}
    )


def confirm_user_registration(confirmation_code: str) -> None:
    try:
        email_confirmation_object = EmailConfirmationCodes.objects.get(code=confirmation_code)
    except EmailConfirmationCodes.DoesNotExist as err:
        raise ConfirmationCodeDoesNotExistError
    
    user = email_confirmation_object.user
    
    if time.time() > email_confirmation_object.expiration:
        email_confirmation_object.delete()
        send_confirmation_email(user=user)
        logger.info(
            msg="The new confirmation code has been sent",
            extra={"new_code": EmailConfirmationCodes.objects.get(user=user), "user": user})
        raise ConfirmationCodeExpiredError
    
   
    user.is_active = True
    user.save()

    email_confirmation_object.delete()
