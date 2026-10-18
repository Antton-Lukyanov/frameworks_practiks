"""Представления списка сдач и карточки сдачи."""

from django.conf import settings
from django.shortcuts import render

from storage import load_students, load_submissions, load_tasks


def _get_submissions():
    """Загрузить сдачи и связанные с ними объекты из JSON-файлов."""
    data_dir = settings.BASE_DIR / "data"
    students = load_students(str(data_dir / "students.json"))
    tasks = load_tasks(str(data_dir / "tasks.json"))
    return load_submissions(
        str(data_dir / "submissions.json"),
        students,
        tasks,
    )


def submission_list(request):
    """Показать сдачи из JSON."""
    submissions = _get_submissions()
    return render(
        request,
        "submissions/submission_list.html",
        {"submissions": submissions},
    )


def submission_detail(request, submission_id):
    """Показать карточку сдачи или шаблон ошибки с HTTP 404."""
    submissions = _get_submissions()
    submission = next(
        (item for item in submissions if item.id == submission_id),
        None,
    )
    return render(
        request,
        "submissions/submission_detail.html",
        {"submission": submission},
        status=404 if submission is None else 200,
    )
