from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import EditProfileDTO
from core.business_logic.errors import (
    InvalidAuthCredentialsError,
    UserAlreadyExistsError,
)
from core.business_logic.services import (
    edit_profile,
    get_countries,
    get_profile_info,
    get_profile_with_reposts_info,
)
from core.presentation_layer.common.converters import convert_data_from_request_to_dto
from core.presentation_layer.web.forms import EditProfileForm
from core.presentation_layer.web.pagination import CustomPagination, PageNotExists
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@require_GET
def profile_controller(request: HttpRequest, username: str) -> HttpResponse:
    """User profile controller."""

    user_profile = get_profile_info(username=username)
    page_number = request.GET.get("page", 1)
    paginator = CustomPagination(per_page=20)
    try:
        tweets_paginated = paginator.paginate(data=user_profile.user_tweets, page_number=page_number)
    except PageNotExists:
        return HttpResponseBadRequest("Page with provided number doesn't exist.")
    context = {
        "profile": user_profile,
        "title": username,
        "tweets": tweets_paginated.data,
    }

    return render(request=request, template_name="profile.html", context=context)


@require_GET
def profile_reposts_controller(request: HttpRequest, username: str) -> HttpResponse:
    """User profile controller."""

    user_profile = get_profile_with_reposts_info(username=username)
    page_number = request.GET.get("page", 1)
    paginator = CustomPagination(per_page=20)
    try:
        tweets_paginated = paginator.paginate(data=user_profile.user_tweets, page_number=page_number)
    except PageNotExists:
        return HttpResponseBadRequest("Page with provided number doesn't exist.")
    context = {
        "profile": user_profile,
        "title": username,
        "tweets": tweets_paginated.data,
    }

    return render(request=request, template_name="profile_reposts.html", context=context)


@require_http_methods(["POST", "GET"])
def edit_profile_controller(request: HttpRequest) -> HttpResponse:
    """
    Controller for editing user profile.
    """

    countries = get_countries()

    profile_initial = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "username": request.user.username,
        "email": request.user.email,
        "birth_date": request.user.birth_date,
        "description": request.user.description,
        "user_id": request.user.pk,
        "old_email": request.user.email,
    }
    if request.user.country:
        country_name = (request.user.country.name,)
        profile_initial["country"] = country_name
    if request.method == "GET":
        form = EditProfileForm(countries=countries, initial=profile_initial)
        context = {"title": "Edit profile", "form": form}
        return render(request=request, template_name="edit_profile.html", context=context)

    else:
        form = EditProfileForm(
            countries,
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            received_data: EditProfileDTO = convert_data_from_request_to_dto(EditProfileDTO, form.cleaned_data)
            try:
                edit_profile(data=received_data)
                if received_data.old_email != received_data.email:
                    logout(request=request)
                    context = {"new_email": received_data.email}
                    return render(request=request, template_name="email_changed.html", context=context)
                return redirect(to="profile", username=received_data.username)
            except UserAlreadyExistsError:
                return HttpResponseBadRequest(content="Such user with entered username or email already exists.")
            except InvalidAuthCredentialsError:
                return HttpResponseBadRequest(
                    content="An incorrect valid password was entered when trying to change the password."
                )
        else:
            context = {"title": "Sign up", "form": form}
            return render(request=request, template_name="edit_profile.html", context=context)
