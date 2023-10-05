from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.services import get_tweets_reposts_from_following_users
from core.presentation_layer.api_v1.pagination import APIPAginator
from core.presentation_layer.api_v1.serializers import TweetSerializer, UserSerialiser
from rest_framework import parsers
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request


@api_view(http_method_names=["GET"])
@parser_classes([parsers.MultiPartParser])
@permission_classes([IsAuthenticated])
def get_following_users_api_controller(request: Request, user_id: int) -> Response:
    order_by = request.query_params.get("order_by", "newest")
    tweets_reposts_dto = get_tweets_reposts_from_following_users(user_id, order_by=order_by)
    following_users = tweets_reposts_dto.following_users
    following_users_serialiser = UserSerialiser(following_users, many=True)
    return Response(data=following_users_serialiser.data)


@api_view(http_method_names=["GET"])
@parser_classes([parsers.MultiPartParser])
@permission_classes([IsAuthenticated])
def get_tweets_from_following_users_api_controller(request: Request, user_id: int) -> Response:
    order_by = request.query_params.get("order_by", "newest")
    tweets_reposts_dto = get_tweets_reposts_from_following_users(user_id, order_by=order_by)
    tweets_from_following_users = tweets_reposts_dto.tweets
    paginator = APIPAginator(per_page=20)
    result_page = paginator.get_paginated_queryset(queryset=tweets_from_following_users, request=request)
    tweets_from_following_users_serialiser = TweetSerializer(result_page, many=True)
    return paginator.paginate(data=tweets_from_following_users_serialiser.data)
