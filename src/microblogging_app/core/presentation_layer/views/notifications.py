from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.services import get_user_notifications
from core.presentation_layer.pagination import CustomPagination, PageNotExists
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from microblogging_app.utils import query_debugger

from .sign_in import sign_in_controller

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@query_debugger
@require_GET
def notifications_controller(request: HttpRequest) -> HttpResponse:
    user = request.user
    if user.is_authenticated:
        user_notifications = get_user_notifications(user=user)

        page_number = request.GET.get("page", 1)
        paginator = CustomPagination(per_page=20)
        try:
            paginated_notifications = paginator.paginate(data=user_notifications, page_number=page_number)
        except PageNotExists:
            return HttpResponseBadRequest("Page with provided number doesn't exist.")
        context = {
            "user": user,
            "notifications": paginated_notifications.data,
        }
        return render(request=request, template_name="notifications.html", context=context)
    else:
        return redirect(sign_in_controller)
