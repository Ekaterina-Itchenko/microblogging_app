from core.presentation_layer import views
from django.urls import path


urlpatterns = [
    path("", views.index_controller, name="home"),
    path("sign_up/", views.registrate_user_controller, name="sign_up"),
    path("confirmation/", views.confirm_registration_controller, name="sign_up_confirmation"),
    path("sign_in/", views.sign_in_controller, name="sign_in"),

]
