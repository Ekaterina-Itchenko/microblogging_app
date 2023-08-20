from core.presentation_layer import views
from core.presentation_layer.views import (
    index_controller,
    like_tweet_controller,
    logout_controller,
    repost_tweet_controller,
    tweet_detail_controller,
)
from django.urls import path

urlpatterns = [
    path("sign_up/", views.registrate_user_controller, name="sign_up"),
    path("confirmation/", views.confirm_registration_controller, name="sign_up_confirmation"),
    path("sign_in/", views.sign_in_controller, name="sign_in"),
    path("logout/", logout_controller, name="logout"),
    path("", index_controller, name="home"),
    path("tweet/<int:tweet_id>/", tweet_detail_controller, name="tweet_detail"),
    path("like/<int:tweet_id>/", like_tweet_controller, name="like_tweet"),
    path("repost/<int:tweet_id>/", repost_tweet_controller, name="repost_tweet"),
]
