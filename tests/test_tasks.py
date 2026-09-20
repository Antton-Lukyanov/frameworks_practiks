"""Тесты класса Task и функций работы с коллекцией заданий."""

from models.tasks import (
    Task, add_task, find_task, get_task_by_id, filter_tasks_by_deadline,
)


def test_task_creation():
    task = Task(1, "Практическая работа №1", 100, "2026-09-15")
    assert task.id == 1
    assert task.title == "Практическая работа №1"
    assert task.max_score == 100
    assert task.deadline == "2026-09-15"


def test_task_str():
    task = Task(1, "Практическая работа №1", 100, "2026-09-15")
    assert "Практическая работа №1" in str(task)


def test_task_is_expired():
    task = Task(1, "ПР1", 100, "2026-09-15")
    assert task.is_expired("2026-10-01")
    assert not task.is_expired("2026-09-01")


def test_add_task():
    tasks = []
    task = add_task(tasks, "Практическая работа №1", 100, "2026-09-15")
    assert len(tasks) == 1
    assert task.id == 1


def test_find_task():
    tasks = []
    add_task(tasks, "Практическая работа №1", 100, "2026-09-15")
    add_task(tasks, "Курсовая работа", 100, "2026-12-01")
    found = find_task(tasks, "практическая")
    assert len(found) == 1
    assert found[0].id == 1


def test_filter_tasks_by_deadline():
    tasks = []
    add_task(tasks, "ПР1", 100, "2026-09-15")
    add_task(tasks, "ПР2", 100, "2026-10-01")
    filtered = filter_tasks_by_deadline(tasks, "2026-09-20")
    assert len(filtered) == 1
    assert filtered[0].title == "ПР1"