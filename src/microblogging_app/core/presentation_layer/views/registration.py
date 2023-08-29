from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import RegistrationDTO
from core.business_logic.errors import (
    ConfirmationCodeDoesNotExistError,
    ConfirmationCodeExpiredError,
    UserAlreadyExistsError,
)
from core.business_logic.services import confirm_user_registration, create_user
from core.presentation_layer.converters import convert_data_from_form_to_dto
from core.presentation_layer.forms import RegistrationForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest


@query_debugger
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
                context = {"new_email": received_data.email}
                render(request=request, template_name="email_changed.html", context=context)
            except UserAlreadyExistsError:
                context = {
                    "title": "Sign up",
                    "form": form,
                    "err_message": "The user with the entered username or email already exists... Please try again.",
                }
                return render(request=request, template_name="registration.html", context=context)
        else:
            context = {"title": "Sign up", "form": form}
            return render(request=request, template_name="registration.html", context=context)


@query_debugger
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
    return redirect(to="sign_in")
