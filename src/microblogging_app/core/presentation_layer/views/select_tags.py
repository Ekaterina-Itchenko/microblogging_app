from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import TagDTO
from core.business_logic.errors import TagNotFound
from core.business_logic.services import get_tweets_by_tag_id
from core.presentation_layer.converters import convert_data_from_form_to_dto
from core.presentation_layer.forms import SelectTagsForm
from core.presentation_layer.pagination import CustomPagination, PageNotExists
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from microblogging_app.utils import query_debugger

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@query_debugger
@require_http_methods(["POST", "GET"])
def select_tag_controller(request: HttpRequest) -> HttpResponse:
    """
    Controller for authentication and authorization.
    """

    if request.method == "GET":
        form = SelectTagsForm()
        context = {"form": form}
        return render(request=request, template_name="select_tags.html", context=context)
    else:
        form = SelectTagsForm(request.POST)
        if form.is_valid():
            received_data = convert_data_from_form_to_dto(TagDTO, form.cleaned_data)

            try:
                tweets, tag = get_tweets_by_tag_id(data=received_data)
            except TagNotFound:
                return HttpResponseBadRequest("Tag doesn't exist.")

            page_number = request.GET.get("page", 1)
            paginator = CustomPagination(per_page=20)
            try:
                tweets_paginated = paginator.paginate(data=tweets, page_number=page_number)
            except PageNotExists:
                return HttpResponseBadRequest("Page with provided number doesn't exist.")

            context = {"tag": tag, "tweets": tweets_paginated.data}
            return render(request=request, template_name="tag_tweets.html", context=context)

        else:
            context = {"form": form}
            return render(request=request, template_name="select_tags.html", context=context)
