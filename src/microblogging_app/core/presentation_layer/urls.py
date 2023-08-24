from core.presentation_layer import views
from django.urls import path

urlpatterns = [
    path("sign_up/", views.registrate_user_controller, name="sign_up"),
    path("confirmation/", views.confirm_registration_controller, name="sign_up_confirmation"),
    path("sign_in/", views.sign_in_controller, name="sign_in"),
    path("logout/", views.logout_controller, name="logout"),
    path("", views.index_controller, name="home"),
    path("tweet/<int:tweet_id>/", views.tweet_detail_controller, name="tweet_detail"),
    path("like/<int:tweet_id>/", views.like_tweet_controller, name="like_tweet"),
    path("repost/<int:tweet_id>/", views.repost_tweet_controller, name="repost_tweet"),
    path("reply/<int:tweet_id>/", views.reply_tweet_controller, name="reply_tweet"),
    path("trending_in_your_country/", views.trending_in_your_country_controller, name="trending_in_your_country"),
    path("tag_tweets/<int:tag_id>/<int:country_id>/", views.get_tweets_from_tag_controller, name="tag_tweets"),
    path("tags/", views.select_tag_controller, name="select_tags"),
]
