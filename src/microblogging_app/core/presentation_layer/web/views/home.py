from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.services import get_tweets_reposts_from_following_users
from core.presentation_layer.web.pagination import CustomPagination, PageNotExists
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@require_http_methods(request_method_list=["GET", "POST"])
def index_controller(request: HttpRequest) -> HttpResponse:
    """
    Display the home page containing tweets and handling tweet creation.

    Args:
        request: The HTTP request.

    Returns:
        HttpResponse: The rendered home page.
    """

    user = request.user
    order_by = request.GET.get("order_by", "newest")
    if user.is_authenticated:
        tweets_reposts_dto = get_tweets_reposts_from_following_users(user, order_by=order_by)
        tweets = tweets_reposts_dto.tweets
        following_users = tweets_reposts_dto.following_users
    else:
        return redirect(to="sign_in")
    page_number = request.GET.get("page", 1)
    paginator = CustomPagination(per_page=20)
    try:
        tweets_paginated = paginator.paginate(data=tweets, page_number=page_number)
    except PageNotExists:
        return HttpResponseBadRequest("Page with provided number doesn't exist.")

    context = {"tweets": tweets_paginated.data, "order_by": order_by, "following_users": following_users}
    return render(request, "home.html", context)
