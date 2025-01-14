from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from . import views


app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.profile_display, name="profile")
]
