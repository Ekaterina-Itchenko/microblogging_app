from core.presentation_layer.api_v1.views import (
    add_tweet_api_controller,
    get_following_users_api_controller,
    get_tweet_replies_api_controller,
    get_tweets_from_following_users_api_controller,
    tweets_api_controller,
)
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Microbloging API",
        default_version="v1",
        description="REST API for microbloging project",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("users/<int:user_id>/following/", get_following_users_api_controller, name="get-following-users-api"),
    path(
        "tweets/<int:user_id>/from_following_users/",
        get_tweets_from_following_users_api_controller,
        name="get-tweets-from-following-users-api",
    ),
    path("tweets/<int:tweet_id>/", tweets_api_controller, name="tweets-api"),
    path("tweets/<int:tweet_id>/replies", get_tweet_replies_api_controller, name="get-tweet-replies-api"),
    path("tweets/", add_tweet_api_controller, name="add-tweet-api"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
