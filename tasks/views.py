"""Страницы списка заданий и карточки задания."""

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.tasks import get_task_by_id
from storage import load_tasks


def task_list(request):
    tasks = load_tasks(str(settings.BASE_DIR / "data/tasks.json"))
    items = "".join(
        '<li class="list-group-item d-flex justify-content-between">'
        f'<a href="/tasks/{task.id}/">{escape(task.title)}</a>'
        '<span class="badge text-bg-primary">'
        f'До {escape(task.deadline)}</span>'
        "</li>"
        for task in tasks
    ) or '<li class="list-group-item text-muted">Заданий пока нет.</li>'
    content = (
        f'<h1 class="mb-4">Задания</h1>'
        f'<ul class="list-group">{items}</ul>'
    )
    return HttpResponse(page("Задания", content))


def task_detail(request, task_id):
    tasks = load_tasks(str(settings.BASE_DIR / "data/tasks.json"))
    task = get_task_by_id(tasks, task_id)
    if task is None:
        content = (
            '<h1 class="text-danger">Задание не найдено</h1>'
            '<a href="/tasks/" class="btn btn-outline-secondary">'
            "К списку заданий</a>"
        )
        return HttpResponse(page("Задание не найдено", content), status=404)

    content = f"""
    <div class="card"><div class="card-body">
        <h1 class="card-title">{escape(task.title)}</h1>
        <p class="card-text"><strong>ID:</strong> {task.id}</p>
        <p class="card-text"><strong>Максимальный балл:</strong>
            {task.max_score}</p>
        <p class="card-text"><strong>Дедлайн:</strong>
            {escape(task.deadline)}</p>
        <a href="/tasks/" class="btn btn-outline-secondary">К списку</a>
    </div></div>
    """
    return HttpResponse(page(task.title, content))
