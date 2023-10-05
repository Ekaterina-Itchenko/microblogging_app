from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import SignInDTO
from core.business_logic.errors import InvalidAuthCredentialsError
from core.business_logic.services import authenticate_user
from core.presentation_layer.common.converters import convert_data_from_request_to_dto
from core.presentation_layer.web.forms import SignInForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@require_http_methods(["POST", "GET"])
def sign_in_controller(request: HttpRequest) -> HttpResponse:
    """
    Controller for authentication and authorization.
    """

    if request.method == "GET":
        form = SignInForm()
        context = {"title": "Sign in", "form": form}
        return render(request=request, template_name="signin.html", context=context)
    else:
        form = SignInForm(request.POST)
        if form.is_valid():
            received_data = convert_data_from_request_to_dto(SignInDTO, form.cleaned_data)
            try:
                user = authenticate_user(data=received_data)
            except InvalidAuthCredentialsError:
                context = {
                    "title": "Sign in",
                    "form": form,
                    "err_message": "Invalid credentials... \n Please try again.",
                }

                return render(request=request, template_name="signin.html", context=context)

            login(request=request, user=user)
            return redirect(to="index")

        else:
            context = {"title": "Sign in", "form": form}
            return render(request=request, template_name="signin.html", context=context)
