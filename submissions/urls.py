from django.urls import path

from . import views


app_name = "submissions"

urlpatterns = [
    path("", views.submission_list, name="list"),
    path("create/", views.submission_create, name="create"),
    path(
        "<int:submission_id>/",
        views.submission_detail,
        name="detail",
    ),
    path("<int:submission_id>/edit/", views.submission_update, name="edit"),
    path("<int:submission_id>/cancel/", views.submission_cancel, name="cancel"),
]

