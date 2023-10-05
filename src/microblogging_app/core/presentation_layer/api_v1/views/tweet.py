from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import AddTweetDTO, EditTweetDTO
from core.business_logic.errors import TweetNotFound
from core.business_logic.services import (
    create_tweet,
    edit_tweet,
    get_replies,
    get_tweet_info,
)
from core.presentation_layer.api_v1.serializers import (
    CreateTweetSerialiser,
    EditTweetSerialiser,
    ErrorSerializer,
    TweetResponseSerialiser,
    TweetSerializer,
)
from core.presentation_layer.common.converters import convert_data_from_request_to_dto
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

if TYPE_CHECKING:
    from rest_framework.request import Request


@swagger_auto_schema(
    method="GET",
    manual_parameters=[openapi.Parameter(name="tweet_id", in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER)],
    responses={
        200: openapi.Response(description="Successfull response", schema=TweetSerializer),
        500: openapi.Response(description="Unhandled server error"),
        404: openapi.Response(description="Resource not found", schema=ErrorSerializer),
    },
)
@swagger_auto_schema(
    method="PATCH",
    manual_parameters=[
        openapi.Parameter(name="tweet_id", in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER),
        openapi.Parameter(name="content", description="Tweet content", in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter(name="tags", in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(description="Successfull response", schema=TweetResponseSerialiser),
        400: openapi.Response(description="Provided invalid data"),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@api_view(http_method_names=["GET", "PATCH"])
@parser_classes([parsers.MultiPartParser])
@permission_classes([IsAuthenticated])
def tweets_api_controller(request: Request, tweet_id: int) -> Response:
    if request.method == "GET":
        try:
            tweet_detail = get_tweet_info(tweet_id=tweet_id)
        except TweetNotFound:
            message = {"message": "Tweet with provided id doesn't exist."}
            return Response(data=message, status=HTTP_404_NOT_FOUND)

        tweet_detail_serialiser = TweetSerializer(tweet_detail)
        return Response(data=tweet_detail_serialiser.data)

    elif request.method == "PATCH":
        serializer = EditTweetSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["tweet_id"] = tweet_id
            data_dto: EditTweetDTO = convert_data_from_request_to_dto(
                dto=EditTweetDTO, data_from_request=serializer.validated_data
            )
            tweet_id = edit_tweet(data=data_dto)
            data: dict[str, str | int] = {"message": "The tweet updated successfully", "tweet_id": tweet_id}
            return Response(data=data)
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="GET",
    responses={
        200: openapi.Response(description="Successful response", schema=TweetSerializer(many=True)),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_tweet_replies_api_controller(request: Request, tweet_id: int) -> Response:
    tweet_replies = get_replies(tweet_id=tweet_id)
    tweet_replies_serialiser = TweetSerializer(tweet_replies, many=True)
    return Response(data=tweet_replies_serialiser.data)


@swagger_auto_schema(
    method="POST",
    manual_parameters=[
        openapi.Parameter(name="content", description="Tweet content", in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter(name="tags", in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(description="Successfull response", schema=TweetResponseSerialiser),
        400: openapi.Response(description="Provided invalid data"),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@api_view(http_method_names=["POST"])
@parser_classes([parsers.MultiPartParser])
@permission_classes([IsAuthenticated])
def add_tweet_api_controller(request: Request) -> Response:
    serializer = CreateTweetSerialiser(data=request.data)
    if serializer.is_valid():
        data = convert_data_from_request_to_dto(dto=AddTweetDTO, data_from_request=serializer.validated_data)
        data.user = request.user
        try:
            tweet_id = create_tweet(data=data)
        except TweetNotFound:
            data = {"message": "The tweet you want to reply doesn't exist."}
            return Response(data=data, status=HTTP_404_NOT_FOUND)
    else:
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    data = {"message": "The tweet created successfully", "tweet_id": tweet_id}
    return Response(data=data)
