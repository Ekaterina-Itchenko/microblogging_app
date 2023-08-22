from core.presentation_layer import views
from django.urls import path

urlpatterns = [
    path("sign_up/", views.registrate_user_controller, name="sign_up"),
    path("confirmation/", views.confirm_registration_controller, name="sign_up_confirmation"),
    path("sign_in/", views.sign_in_controller, name="sign_in"),
    path("trending_in_your_country/", views.trending_in_your_country_controller, name="trending_in_your_country"),
    path("tag_tweets/<int:tag_id>/<int:country_id>/", views.get_tweets_from_tag_controller, name="tag_tweets"),
]
