"""Представления списка студентов и карточки студента."""

from django.conf import settings
from django.shortcuts import render

from models.students import get_student_by_id
from storage import load_students


def student_list(request):
    """Показать студентов, загруженных из JSON."""
    filename = settings.BASE_DIR / "data/students.json"
    students = load_students(str(filename))
    return render(request, "students/student_list.html", {"students": students})


def student_detail(request, student_id):
    """Показать карточку студента или шаблон ошибки с HTTP 404."""
    filename = settings.BASE_DIR / "data/students.json"
    students = load_students(str(filename))
    student = get_student_by_id(students, student_id)
    return render(
        request,
        "students/student_detail.html",
        {"student": student},
        status=404 if student is None else 200,
    )
