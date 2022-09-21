from . import views
from django.urls import path


urlpatterns = [
    path("", views.cpanel, name="cpanel"),
    path("upload-article", views.uploadArticle, name="uploadarticle"),
]
