"""Корневая маршрутизация Django-проекта."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("students/", include("students.urls")),
    path("tasks/", include("tasks.urls")),
    path("submissions/", include("submissions.urls")),
]

handler404 = "homepage.views.page_not_found"
