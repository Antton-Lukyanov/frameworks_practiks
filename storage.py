"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
import os


def _load_json(filename: str) -> list[dict]:
    """Загрузить список словарей из JSON-файла.

    При отсутствии файла или некорректном JSON вернуть пустой список.
    """
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


def load_students(filename: str) -> list[dict]:
    """Загрузить студентов из JSON-файла."""
    return _load_json(filename)


def save_students(filename: str, students: list[dict]) -> None:
    """Сохранить студентов в JSON-файл."""
    _save_json(filename, students)


def load_tasks(filename: str) -> list[dict]:
    """Загрузить задания из JSON-файла."""
    return _load_json(filename)


def save_tasks(filename: str, tasks: list[dict]) -> None:
    """Сохранить задания в JSON-файл."""
    _save_json(filename, tasks)


def load_submissions(filename: str) -> list[dict]:
    """Загрузить сдачи из JSON-файла."""
    return _load_json(filename)


def save_submissions(filename: str, submissions: list[dict]) -> None:
    """Сохранить сдачи в JSON-файл."""
    _save_json(filename, submissions)