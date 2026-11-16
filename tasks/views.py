"""Task list and detail pages backed by SQLite."""

from django.shortcuts import render

from db.queries import fetch_task, fetch_tasks


def task_list(request):
    return render(request, "tasks/task_list.html", {"tasks": fetch_tasks()})


def task_detail(request, task_id):
    task = fetch_task(task_id)
    return render(
        request,
        "tasks/task_detail.html",
        {"task": task},
        status=404 if task is None else 200,
    )
