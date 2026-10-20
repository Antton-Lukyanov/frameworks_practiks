from django.urls import path

from . import views


app_name = "submissions"

urlpatterns = [
    path("", views.submission_list, name="list"),
    path(
        "<int:submission_id>/",
        views.submission_detail,
        name="detail",
    ),
]

