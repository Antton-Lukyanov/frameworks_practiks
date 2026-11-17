from django.contrib import admin

from submissions.models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "task",
        "file_name",
        "score",
        "is_passing",
        "submission_date",
        "status",
    )
    list_filter = ("status", "submission_date", "task")
    search_fields = ("student__name", "task__title", "file_name")
    autocomplete_fields = ("student", "task")
    ordering = ("-submission_date", "-id")
    date_hierarchy = "submission_date"
    list_select_related = ("student", "task")
    list_per_page = 25
