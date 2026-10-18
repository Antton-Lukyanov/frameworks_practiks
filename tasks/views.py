"""Представления списка заданий и карточки задания."""

from django.conf import settings
from django.shortcuts import render

from models.tasks import get_task_by_id
from storage import load_tasks


def task_list(request):
    """Показать учебные задания, загруженные из JSON."""
    tasks = load_tasks(str(settings.BASE_DIR / "data/tasks.json"))
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_detail(request, task_id):
    """Показать карточку задания или шаблон ошибки с HTTP 404."""
    tasks = load_tasks(str(settings.BASE_DIR / "data/tasks.json"))
    task = get_task_by_id(tasks, task_id)
    return render(
        request,
        "tasks/task_detail.html",
        {"task": task},
        status=404 if task is None else 200,
    )
