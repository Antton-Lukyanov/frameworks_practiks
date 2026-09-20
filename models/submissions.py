"""Класс Submission и функции работы с коллекцией сдач.

Функции get_task_status(), check_file_size() и get_result()
перенесены из ПР1/ПР2 и остаются обычными функциями:
они не относятся к состоянию конкретного объекта.
"""

from __future__ import annotations

from datetime import date

from .students import Student
from .tasks import Task


class Submission:
    """Факт сдачи задания студентом."""

    def __init__(
        self,
        submission_id: int,
        student: Student,
        task: Task,
        file_name: str,
        file_size_mb: float,
        score: int = 0,
        submission_date: str | None = None,
    ) -> None:
        """Создать объект сдачи."""
        self.id = submission_id
        self.student = student
        self.task = task
        self.file_name = file_name
        self.file_size_mb = file_size_mb
        self.score = score
        self.submission_date = submission_date or date.today().isoformat()
        self.is_cancelled = False

    def __str__(self) -> str:
        """Вернуть строковое представление сдачи."""
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"[{self.id}] {self.student.name} → {self.task.title}, "
            f"файл {self.file_name} ({self.file_size_mb} МБ), "
            f"балл {self.score}, дата {self.submission_date}, {status}"
        )

    def cancel(self) -> None:
        """Отменить сдачу, изменив её состояние."""
        self.is_cancelled = True

    def get_result(self) -> str:
        """Вернуть текстовый результат по баллам."""
        return get_result(self.score)

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "student_id": self.student.id,
            "task_id": self.task.id,
            "file_name": self.file_name,
            "file_size_mb": self.file_size_mb,
            "score": self.score,
            "submission_date": self.submission_date,
            "is_cancelled": self.is_cancelled,
        }

    @classmethod
    def from_data(
        cls,
        data: dict,
        students: list[Student],
        tasks: list[Task],
    ) -> "Submission | None":
        """Создать сдачу из словаря, найдя связанные объекты Student и Task."""
        student = next((s for s in students if s.id == data["student_id"]), None)
        task = next((t for t in tasks if t.id == data["task_id"]), None)
        if student is None or task is None:
            return None
        submission = cls(
            submission_id=data["id"],
            student=student,
            task=task,
            file_name=data["file_name"],
            file_size_mb=data["file_size_mb"],
            score=data["score"],
            submission_date=data["submission_date"],
        )
        submission.is_cancelled = data.get("is_cancelled", False)
        return submission


# ---------- Функции, перенесённые из ПР1 (не методы) ----------

def get_task_status(is_submitted: bool) -> str:
    """Вернуть текстовый статус сдачи задания."""
    if is_submitted:
        return "Задание сдано"
    return "Задание не сдано"


def check_file_size(file_size_mb: float) -> str:
    """Проверить допустимый размер файла (макс. 10 МБ)."""
    if file_size_mb > 10:
        return "Файл слишком большой (макс. 10 МБ)"
    return "Файл допустимого размера"


def get_result(score: int) -> str:
    """Выставить результат по баллам."""
    if score >= 80:
        return "Отлично"
    elif score >= 60:
        return "Хорошо"
    else:
        return "Требуется доработка"


# ---------- Функции работы с коллекцией объектов Submission ----------

def is_task_submitted(submissions: list[Submission], student: Student, task: Task) -> bool:
    """Проверить, сдано ли задание студентом (учитываются только активные сдачи)."""
    for s in submissions:
        if s.student.id == student.id and s.task.id == task.id and not s.is_cancelled:
            return True
    return False


def create_submission(
    submissions: list[Submission],
    student: Student,
    task: Task,
    file_name: str,
    file_size_mb: float,
) -> Submission | None:
    """Создать новую сдачу. Вернуть None, если задание уже сдано."""
    if is_task_submitted(submissions, student, task):
        return None
    submission_id = max((s.id for s in submissions), default=0) + 1
    submission = Submission(
        submission_id=submission_id,
        student=student,
        task=task,
        file_name=file_name,
        file_size_mb=file_size_mb,
    )
    submissions.append(submission)
    return submission


def cancel_submission(submissions: list[Submission], submission_id: int) -> bool:
    """Отменить сдачу по ID. Вернуть True, если сдача найдена."""
    for s in submissions:
        if s.id == submission_id:
            s.cancel()
            return True
    return False


def get_statistics(submissions: list[Submission]) -> dict:
    """Вернуть статистику по сдачам."""
    if not submissions:
        return {"total": 0, "submitted": 0, "average_score": 0.0}
    active = [s for s in submissions if not s.is_cancelled]
    scored = [s for s in active if s.score > 0]
    return {
        "total": len(active),
        "submitted": len(scored),
        "average_score": sum(s.score for s in scored) / len(scored) if scored else 0.0,
    }


def show_submissions(submissions: list[Submission]) -> None:
    """Вывести список сдач."""
    if not submissions:
        print("Список сдач пуст.")
        return
    print("\n--- Сдачи ---")
    for s in submissions:
        print(s)