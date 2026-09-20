"""Пакет моделей предметной области «Сервис сдачи заданий»."""

from .students import Student
from .tasks import Task
from .submissions import Submission

__all__ = ["Student", "Task", "Submission"]