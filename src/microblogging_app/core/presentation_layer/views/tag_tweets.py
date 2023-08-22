from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.services import get_tweets_from_tag_id
from django.core.paginator import EmptyPage, Paginator
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@require_GET
@query_debugger
def get_tweets_from_tag_controller(request: HttpRequest, tag_id: int, country_id: int) -> HttpResponse:
    """Controller to display tweets related with paticular tag."""

    try:
        page_number = request.GET["page"]
    except KeyError:
        logger.info(msg="Page query parameter does not exist.", extra={"query parameters": request.GET})
        page_number = 1

    tweets = get_tweets_from_tag_id(tag_id=tag_id, country_id=country_id)
    paginator = Paginator(tweets, 1)

    try:
        tweets_paginated = paginator.page(page_number)
    except EmptyPage:
        logger.error(msg="Page number does not exist.", extra={"Page number": page_number})
        return HttpResponseBadRequest("Page number does not exist.")

    if tweets_paginated.has_next():
        next_page = tweets_paginated.next_page_number()
    else:
        next_page = None

    if tweets_paginated.has_previous():
        previous_page = tweets_paginated.previous_page_number()
    else:
        previous_page = None

    last_page = paginator.num_pages

    context = {
        "previous_page": previous_page,
        "next_page": next_page,
        "last_page": last_page,
        "tweets": tweets_paginated,
        "tag_id": tag_id,
        "country_id": country_id,
    }
    return render(request=request, template_name="tag_tweets.html", context=context)
