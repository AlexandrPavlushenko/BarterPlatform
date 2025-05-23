from django.contrib.auth.views import LogoutView
from django.urls import path

from .apps import UsersConfig
from .views import (
    ActivateView,
    CustomLoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    UserCreateView,
    UserProfileUpdateView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("profile/", UserProfileUpdateView.as_view(), name="profile"),
    path("password_reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]