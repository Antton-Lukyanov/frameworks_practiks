from django.contrib import admin

from submissions.models import Submission
from tasks.models import Task


class TaskSubmissionInline(admin.TabularInline):
    model = Submission
    fk_name = "task"
    extra = 0
    fields = ("student", "file_name", "score", "status", "submission_date")
    autocomplete_fields = ("student",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "max_score", "deadline", "slug")
    list_filter = ("deadline",)
    search_fields = ("title",)
    ordering = ("deadline", "id")
    readonly_fields = ("slug",)
    list_per_page = 25
    inlines = (TaskSubmissionInline,)
