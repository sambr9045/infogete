from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landingpage.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("cpanel/", include("cpanel.urls")),
    path("tinymce/", include("tinymce.urls")),
]
