"""Страницы списка сдач и карточки сдачи."""

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from storage import load_students, load_submissions, load_tasks


def _get_submissions():
    data_dir = settings.BASE_DIR / "data"
    students = load_students(str(data_dir / "students.json"))
    tasks = load_tasks(str(data_dir / "tasks.json"))
    submissions = load_submissions(
        str(data_dir / "submissions.json"), students, tasks
    )
    return submissions


def _submission_item(submission):
    badge = (
        "text-bg-secondary" if submission.is_cancelled else "text-bg-success"
    )
    status = "Отменена" if submission.is_cancelled else "Активна"
    return (
        '<li class="list-group-item d-flex justify-content-between">'
        f'<a href="/submissions/{submission.id}/">'
        f'{escape(submission.student.name)} — {escape(submission.task.title)}'
        "</a>"
        f'<span class="badge {badge}">{status}</span>'
        "</li>"
    )


def submission_list(request):
    submissions = _get_submissions()
    items = "".join(_submission_item(item) for item in submissions)
    if not items:
        items = '<li class="list-group-item text-muted">Сдач пока нет.</li>'
    content = (
        f'<h1 class="mb-4">Сдачи заданий</h1>'
        f'<ul class="list-group">{items}</ul>'
    )
    return HttpResponse(page("Сдачи заданий", content))


def submission_detail(request, submission_id):
    submission = next(
        (item for item in _get_submissions() if item.id == submission_id),
        None,
    )
    if submission is None:
        content = (
            '<h1 class="text-danger">Сдача не найдена</h1>'
            '<a href="/submissions/" class="btn btn-outline-secondary">'
            "К списку сдач</a>"
        )
        return HttpResponse(page("Сдача не найдена", content), status=404)

    badge = (
        "text-bg-secondary" if submission.is_cancelled else "text-bg-success"
    )
    status = "Отменена" if submission.is_cancelled else "Активна"
    content = f"""
    <div class="card"><div class="card-body">
        <h1 class="card-title">Сдача №{submission.id}</h1>
        <p class="card-text"><strong>Студент:</strong>
            {escape(submission.student.name)}</p>
        <p class="card-text"><strong>Задание:</strong>
            {escape(submission.task.title)}</p>
        <p class="card-text"><strong>Файл:</strong>
            {escape(submission.file_name)} ({submission.file_size_mb} МБ)</p>
        <p class="card-text"><strong>Дата:</strong>
            {escape(submission.submission_date)}</p>
        <p class="card-text"><strong>Результат:</strong>
            {escape(submission.get_result())} ({submission.score} баллов)</p>
        <p class="card-text"><strong>Статус:</strong>
            <span class="badge {badge}">{status}</span></p>
        <a href="/submissions/" class="btn btn-outline-secondary">К списку</a>
    </div></div>
    """
    return HttpResponse(page(f"Сдача №{submission.id}", content))
