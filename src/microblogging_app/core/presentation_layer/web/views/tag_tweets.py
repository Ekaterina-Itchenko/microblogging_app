from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.services import get_tweets_by_tag_name_country_name
from core.presentation_layer.web.pagination import CustomPagination, PageNotExists
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@require_GET
def get_tweets_by_tag_country_controller(request: HttpRequest, tag_name: str, country_name: str) -> HttpResponse:
    """Controller to display tweets related with passed tag in your country."""

    try:
        page_number = request.GET["page"]
    except KeyError:
        logger.info(msg="Page query parameter does not exist.", extra={"query parameters": request.GET})
        page_number = 1

    tweets = get_tweets_by_tag_name_country_name(tag_name=tag_name, country_name=country_name)
    page_number = request.GET.get("page", 1)
    paginator = CustomPagination(per_page=20)
    try:
        tweets_paginated = paginator.paginate(data=tweets, page_number=page_number)
    except PageNotExists:
        return HttpResponseBadRequest("Page with provided number doesn't exist.")

    context = {"tag_name": tag_name, "tweets": tweets_paginated.data}
    return render(request=request, template_name="tag_tweets.html", context=context)
