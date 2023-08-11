from __future__ import annotations

from core.presentation_layer.forms import RegistrationForm
from core.presentation_layer.converters import convert_data_from_form_to_dto
from core.business_logic.dto import RegistrationDTO
from core.presentation_layer.views import sign_in_controller
from core.business_logic.services import create_user, confirm_user_registration
from core.business_logic.errors import (
    UserAlreadyExistsError,
    ConfirmationCodeDoesNotExistError,
    ConfirmationCodeExpiredError
)

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET", "POST"])
def registrate_user_controller(request: HttpRequest) -> HttpResponse:
    """
    Controller for registration.
    """

    if request.method == "GET":
        form = RegistrationForm()
        context = {"title": "Sign up", "form": form}
        return render(request=request, template_name="registration.html", context=context)
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            received_data = convert_data_from_form_to_dto(RegistrationDTO, form.cleaned_data)
            try:
                create_user(received_data=received_data)
                return HttpResponse(
                    content="The confirmation link has been sent to your email."
                    "Please follow this link to confirm your registration"
                )
            except UserAlreadyExistsError:
                return HttpResponseBadRequest(content="Such user already exists. Invalid username or password.")

        else:
            context = {"title": "Sign up", "form": form}
            return render(request=request, template_name="registration.html", context=context)


@require_http_methods(["GET"])
def confirm_registration_controller(request: HttpRequest) -> HttpResponse:
    """
    Controller to confirm a registration. After a confirmation redirects to the authentication page.
    """

    received_code = request.GET["code"]
    try:
        confirm_user_registration(confirmation_code=received_code)
    except ConfirmationCodeDoesNotExistError:
        return HttpResponseBadRequest(content="Invalid confirmation code")
    except ConfirmationCodeExpiredError:
        return HttpResponseBadRequest(
            content="The confirmation code is expired. The new confirmation link has been sent to your email."
                    "Please follow this link to confirm your registration."
        )
    return redirect(to=sign_in_controller)
