"""Тесты функций работы с заданиями."""

from tasks import add_task, find_task, filter_tasks_by_deadline


def test_add_task():
    tasks = []
    add_task(tasks, "Практическая работа №1", 100, "2026-09-15")
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Практическая работа №1"
    assert tasks[0]["max_score"] == 100


def test_find_task():
    tasks = []
    add_task(tasks, "Практическая работа №1", 100, "2026-09-15")
    add_task(tasks, "Курсовая работа", 100, "2026-12-01")
    found = find_task(tasks, "практическая")
    assert len(found) == 1
    assert found[0]["id"] == 1


def test_filter_tasks_by_deadline():
    tasks = []
    add_task(tasks, "ПР1", 100, "2026-09-15")
    add_task(tasks, "ПР2", 100, "2026-10-01")
    filtered = filter_tasks_by_deadline(tasks, "2026-09-20")
    assert len(filtered) == 1
    assert filtered[0]["title"] == "ПР1"