"""Сохранение и загрузка данных проекта в JSON-файлах.

Модуль работает с коллекциями объектов Student, Task, Submission.
При загрузке JSON преобразуется в объекты; при сохранении — обратно.
"""

from __future__ import annotations

import json
import os

from models.students import Student
from models.tasks import Task
from models.submissions import Submission


def _load_json(filename: str) -> list[dict]:
    """Загрузить список словарей из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка чтения файла {filename}: {error}")
        return []


def _save_json(filename: str, data: list[dict]) -> None:
    """Сохранить список словарей в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка записи файла {filename}: {error}")


def load_students(filename: str) -> list[Student]:
    """Загрузить студентов из JSON-файла как объекты Student."""
    return [Student.from_data(d) for d in _load_json(filename)]


def save_students(filename: str, students: list[Student]) -> None:
    """Сохранить объекты Student в JSON-файл."""
    _save_json(filename, [s.to_data() for s in students])


def load_tasks(filename: str) -> list[Task]:
    """Загрузить задания из JSON-файла как объекты Task."""
    return [Task.from_data(d) for d in _load_json(filename)]


def save_tasks(filename: str, tasks: list[Task]) -> None:
    """Сохранить объекты Task в JSON-файл."""
    _save_json(filename, [t.to_data() for t in tasks])


def load_submissions(
    filename: str,
    students: list[Student],
    tasks: list[Task],
) -> list[Submission]:
    """Загрузить сдачи из JSON-файла как объекты Submission.

    Для восстановления связей объект Submission требует коллекции
    студентов и заданий.
    """
    submissions: list[Submission] = []
    for d in _load_json(filename):
        submission = Submission.from_data(d, students, tasks)
        if submission is not None:
            submissions.append(submission)
    return submissions


def save_submissions(filename: str, submissions: list[Submission]) -> None:
    """Сохранить объекты Submission в JSON-файл."""
    _save_json(filename, [s.to_data() for s in submissions])