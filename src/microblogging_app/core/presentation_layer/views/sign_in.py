from __future__ import annotations
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest
from core.presentation_layer.forms import SignInForm
from core.presentation_layer.converters import convert_data_from_form_to_dto
from .index import index_controller
from core.business_logic.errors import InvalidAuthCredentialsError
from django.contrib.auth import login
from core.business_logic.services import authenticate_user
from core.business_logic.dto import SignInDTO
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@require_http_methods(["POST", "GET"])
def sign_in_controller(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = SignInForm()
        logger.info("Sign in empty form is sent")
        context = {"title": "Sign in", "form": form}
        return render(request=request, template_name="signin.html", context=context)
    else:
        form = SignInForm(request.POST)

        if form.is_valid():
            received_data = convert_data_from_form_to_dto(SignInDTO, form.cleaned_data)
            logger.info(f"Sign in form data is converted to DTO: {received_data}")
            try:
                logger.info("Data is sent to authentication")
                user = authenticate_user(data=received_data)
            except InvalidAuthCredentialsError:
                return HttpResponseBadRequest(content="Invalid credentials.")
            
            login(request=request, user=user)
            return redirect(to=index_controller)
 
        else:
            context = {"title": "Sign up", "form": form}
            return render(request=request, template_name="signin.html", context=context)
