from django.urls import path, include
from landingpage import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("signup", views.sign_up, name="signup"),
    path("confirm-email/<uuid4>/", views.confirmEmail, name="confirmemail"),
    # reset password
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="reset_password/reset_password.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="reset_password/reset_password_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="reset_password/reset_password_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="reset_password/reset_password_completed.html"
        ),
        name="password_reset_complete",
    ),
]
