from django.contrib import admin

from students.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "group")
    list_filter = ("group",)
    search_fields = ("name", "group")
