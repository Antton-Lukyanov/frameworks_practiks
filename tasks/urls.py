from django.urls import path

from . import views


app_name = "tasks"

urlpatterns = [
    path("", views.task_list, name="list"),
    path("<slug:slug>/", views.task_detail, name="detail"),
]
