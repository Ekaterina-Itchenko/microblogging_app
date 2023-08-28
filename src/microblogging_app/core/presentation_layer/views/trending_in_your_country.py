from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.services import get_most_popular_tags
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_GET
@query_debugger
def trending_in_your_country_controller(request: HttpRequest) -> HttpResponse:
    """Controller to display data 10 popular tags in user's country"""

    user = request.user
    if user.is_authenticated:
        if user.country:
            country_name = user.country.name
            popular_tags = get_most_popular_tags(country_name=country_name)
            context = {"tags": popular_tags, "country_name": country_name}
            return render(request=request, template_name="trending_in_your_country.html", context=context)
        else:
            context = {"country_not_exist": True}
            render(request=request, template_name="trending_in_your_country.html", context=context)
            return render(request=request, template_name="trending_in_your_country.html", context=context)
    else:
        return redirect("sign_in")
