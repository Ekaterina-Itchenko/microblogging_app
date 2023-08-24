from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.errors import CountryNotEnteredError
from core.business_logic.services import get_most_popular_tags
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from microblogging_app.utils import query_debugger

from .sign_in import sign_in_controller

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_GET
@query_debugger
def trending_in_your_country_controller(request: HttpRequest) -> HttpResponse:
    """Controller to display data 10 popular tags in user's country"""

    user = request.user
    if user.is_authenticated:
        country_id = user.country_id
        try:
            popular_tags = get_most_popular_tags(country_id=country_id)
            context = {"tags": popular_tags, "country_id": country_id}
            return render(request=request, template_name="trending_in_your_country.html", context=context)
        except CountryNotEnteredError:
            return HttpResponseBadRequest("Please, enter a country in your profile to see the data in this page.")
    else:
        return redirect(sign_in_controller)