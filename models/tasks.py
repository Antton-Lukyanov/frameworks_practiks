"""Класс Task и функции работы с коллекцией заданий."""

from __future__ import annotations

from datetime import date


class Task:
    """Учебное задание."""

    def __init__(self, task_id: int, title: str, max_score: int, deadline: str) -> None:
        """Создать объект задания."""
        self.id = task_id
        self.title = title
        self.max_score = max_score
        self.deadline = deadline

    def __str__(self) -> str:
        """Вернуть строковое представление задания."""
        return f"[{self.id}] {self.title} (макс. {self.max_score} б., до {self.deadline})"

    def is_expired(self, current_date: str) -> bool:
        """Проверить, истёк ли срок сдачи задания."""
        return date.fromisoformat(current_date) > date.fromisoformat(self.deadline)

    @classmethod
    def from_data(cls, data: dict) -> "Task":
        """Создать задание из словаря (данные из JSON)."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            max_score=data["max_score"],
            deadline=data["deadline"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "max_score": self.max_score,
            "deadline": self.deadline,
        }


def add_task(tasks: list[Task], title: str, max_score: int, deadline: str) -> Task:
    """Создать задание и добавить его в коллекцию. Вернуть объект."""
    task_id = max((t.id for t in tasks), default=0) + 1
    task = Task(task_id, title, max_score, deadline)
    tasks.append(task)
    return task


def find_task(tasks: list[Task], query: str) -> list[Task]:
    """Найти задания по подстроке названия (без учёта регистра)."""
    query_lower = query.lower()
    return [t for t in tasks if query_lower in t.title.lower()]


def get_task_by_id(tasks: list[Task], task_id: int) -> Task | None:
    """Вернуть задание по ID или None."""
    for t in tasks:
        if t.id == task_id:
            return t
    return None


def filter_tasks_by_deadline(tasks: list[Task], deadline: str) -> list[Task]:
    """Отобрать задания с дедлайном не позже указанной даты."""
    limit = date.fromisoformat(deadline)
    return [t for t in tasks if date.fromisoformat(t.deadline) <= limit]


def show_tasks(tasks: list[Task]) -> None:
    """Вывести список заданий."""
    if not tasks:
        print("Список заданий пуст.")
        return
    print("\n--- Задания ---")
    for t in tasks:
        print(t)