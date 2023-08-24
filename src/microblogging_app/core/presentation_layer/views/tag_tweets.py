from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.services import get_tweets_from_tag_id
from core.presentation_layer.pagination import CustomPagination, PageNotExists
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@query_debugger
@require_GET
def get_tweets_from_tag_controller(request: HttpRequest, tag_id: int, country_id: int) -> HttpResponse:
    """Controller to display tweets related with paticular tag."""

    tweets, tag = get_tweets_from_tag_id(tag_id=tag_id, country_id=country_id)

    page_number = request.GET.get("page", 1)
    paginator = CustomPagination(per_page=20)
    try:
        tweets_paginated = paginator.paginate(data=tweets, page_number=page_number)
    except PageNotExists:
        return HttpResponseBadRequest("Page with provided number doesn't exist.")

    context = {
        "tag": tag,
        "tweets": tweets_paginated.data,
    }
    return render(request=request, template_name="tag_tweets.html", context=context)
