"""Страницы списка студентов и карточки студента."""

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.students import get_student_by_id
from storage import load_students


def student_list(request):
    students = load_students(str(settings.BASE_DIR / "data/students.json"))
    items = "".join(
        '<li class="list-group-item">'
        f'<a href="/students/{student.id}/">{escape(student.name)}</a>'
        f'<span class="text-muted ms-2">{escape(student.group)}</span>'
        "</li>"
        for student in students
    ) or '<li class="list-group-item text-muted">Студентов пока нет.</li>'
    content = (
        f'<h1 class="mb-4">Студенты</h1>'
        f'<ul class="list-group">{items}</ul>'
    )
    return HttpResponse(page("Студенты", content))


def student_detail(request, student_id):
    students = load_students(str(settings.BASE_DIR / "data/students.json"))
    student = get_student_by_id(students, student_id)
    if student is None:
        content = (
            '<h1 class="text-danger">Студент не найден</h1>'
            '<a href="/students/" class="btn btn-outline-secondary">'
            "К списку студентов</a>"
        )
        return HttpResponse(page("Студент не найден", content), status=404)

    content = f"""
    <div class="card"><div class="card-body">
        <h1 class="card-title">{escape(student.name)}</h1>
        <p class="card-text"><strong>ID:</strong> {student.id}</p>
        <p class="card-text"><strong>Группа:</strong>
            {escape(student.group)}</p>
        <a href="/students/" class="btn btn-outline-secondary">К списку</a>
    </div></div>
    """
    return HttpResponse(page(student.name, content))
