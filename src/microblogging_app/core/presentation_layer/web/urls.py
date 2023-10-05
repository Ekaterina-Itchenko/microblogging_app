from core.presentation_layer.web import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("sign_up/", views.registrate_user_controller, name="sign_up"),
    path("confirmation/", views.confirm_registration_controller, name="sign_up_confirmation"),
    path("sign_in/", views.sign_in_controller, name="sign_in"),
    path("tweet/<int:tweet_id>/", views.tweet_detail_controller, name="tweet_detail"),
    path("like/<int:tweet_id>/", views.like_tweet_controller, name="like_tweet"),
    path("repost/<int:tweet_id>/", views.repost_tweet_controller, name="repost_tweet"),
    path("trending_in_your_country/", views.trending_in_your_country_controller, name="trending_in_your_country"),
    path(
        "tag_tweets/<str:country_name>/<str:tag_name>/", views.get_tweets_by_tag_country_controller, name="tag_tweets"
    ),
    path("tags/", views.select_tag_controller, name="select_tags"),
    path("<str:username>/profile/", views.profile_controller, name="profile"),
    path("<str:username>/profile/with_reposts/", views.profile_reposts_controller, name="profile_reposts"),
    path("", views.index_controller, name="index"),
    path("logout/", views.logout_controller, name="logout"),
    path("add_post/", views.add_tweet_controller, name="add_post"),
    path("<str:username>/follow/", views.follow_controller, name="follow"),
    path("<str:username>/unfollow/", views.unfollow_controller, name="unfollow"),
    path("<str:username>/followers/", views.followers_controller, name="followers"),
    path("<str:username>/following/", views.following_controller, name="following"),
    path("reply/<int:tweet_id>/", views.reply_tweet_controller, name="reply_tweet"),
    path("tweet/<int:tweet_id>/edit", views.edit_tweet_controller, name="tweet_edit"),
    path("profile/edit", views.edit_profile_controller, name="profile_edit"),
    path("tweet/<int:tweet_id>/liked_by/", views.tweet_detail_controller_likes, name="tweet_detail_likes"),
    path("tweet/<int:tweet_id>/reposted_by/", views.tweet_detail_controller_reposts, name="tweet_detail_reposts"),
    path("notifications/", views.notifications_controller, name="notifications"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
