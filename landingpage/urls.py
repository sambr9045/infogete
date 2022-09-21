from django.urls import path, include
from landingpage import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("signup", views.sign_up, name="signup"),
    path("confirm-email/<uuid4>/", views.confirmEmail, name="confirmemail"),
]
