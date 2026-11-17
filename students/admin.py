from django.contrib import admin

from submissions.models import Submission
from students.models import Student


class StudentSubmissionInline(admin.TabularInline):
    model = Submission
    fk_name = "student"
    extra = 0
    fields = ("task", "file_name", "score", "status", "submission_date")
    autocomplete_fields = ("task",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "group")
    list_filter = ("group",)
    search_fields = ("name", "group")
    ordering = ("name", "id")
    list_per_page = 25
    inlines = (StudentSubmissionInline,)
