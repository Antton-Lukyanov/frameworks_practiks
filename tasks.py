"""Функции для работы с заданиями."""

from datetime import date


def add_task(tasks: list[dict], title: str, max_score: int, deadline: str) -> None:
    """Добавить задание в список tasks."""
    task_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({
        "id": task_id,
        "title": title,
        "max_score": max_score,
        "deadline": deadline,
    })


def find_task(tasks: list[dict], query: str) -> list[dict]:
    """Найти задания по подстроке названия (без учёта регистра)."""
    query_lower = query.lower()
    return [t for t in tasks if query_lower in t["title"].lower()]


def filter_tasks_by_deadline(tasks: list[dict], deadline: str) -> list[dict]:
    """Отобрать задания с дедлайном не позже указанной даты."""
    limit = date.fromisoformat(deadline)
    return [t for t in tasks if date.fromisoformat(t["deadline"]) <= limit]