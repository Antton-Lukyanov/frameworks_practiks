from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "max_score", "deadline")
    list_filter = ("deadline",)
    search_fields = ("title",)
    ordering = ("deadline", "id")
