from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import TagDTO
from core.business_logic.errors import TagNotFound
from core.business_logic.services import get_tags_func, get_tweets_by_tag_name
from core.presentation_layer.common.converters import convert_data_from_request_to_dto
from core.presentation_layer.web.forms import SelectTagsForm
from core.presentation_layer.web.pagination import CustomPagination, PageNotExists
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def select_tag_controller(request: HttpRequest) -> HttpResponse:
    """
    Controller for authentication and authorization.
    """

    tags = get_tags_func()
    form = SelectTagsForm(tags, request.GET)
    if form.is_valid():
        received_data = convert_data_from_request_to_dto(TagDTO, form.cleaned_data)

        try:
            tag_tweet_dto = get_tweets_by_tag_name(data=received_data)
            tweets = tag_tweet_dto.tweets
            tag = tag_tweet_dto.tag
        except TagNotFound:
            logger.info(msg="The tag was not specified.")
            empty_context = {"form": form}
            return render(request=request, template_name="tag.html", context=empty_context)

        page_number = request.GET.get("page", 1)
        paginator = CustomPagination(per_page=20)
        try:
            tweets_paginated = paginator.paginate(data=tweets, page_number=page_number)
        except PageNotExists:
            return HttpResponseBadRequest("Page with provided number doesn't exist.")

        context = {"tag_name": tag.name, "tweets": tweets_paginated.data, "form": form}
        return render(request=request, template_name="tag.html", context=context)

    else:
        context = {"form": form}
        return render(request=request, template_name="tag.html", context=context)
