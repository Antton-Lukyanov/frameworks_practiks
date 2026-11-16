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
        "submission_date",
        "is_cancelled",
    )
    list_filter = ("is_cancelled", "submission_date", "task")
    search_fields = ("student__name", "task__title", "file_name")
    autocomplete_fields = ("student", "task")
