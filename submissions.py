"""Функции для работы со сдачами заданий.

Функции get_task_status(), check_file_size() и get_result()
перенесены из ПР1 без изменения логики.
"""

from datetime import date


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


def is_task_submitted(submissions: list[dict], student_id: int, task_id: int) -> bool:
    """Проверить, сдано ли задание студентом."""
    for s in submissions:
        if s["student_id"] == student_id and s["task_id"] == task_id:
            return True
    return False


def create_submission(
    submissions: list[dict],
    student_id: int,
    task_id: int,
    file_name: str,
    file_size_mb: float,
) -> dict | None:
    """Создать новую сдачу. Вернуть None, если задание уже сдано."""
    if is_task_submitted(submissions, student_id, task_id):
        return None
    submission_id = max((s["id"] for s in submissions), default=0) + 1
    submission = {
        "id": submission_id,
        "student_id": student_id,
        "task_id": task_id,
        "file_name": file_name,
        "file_size_mb": file_size_mb,
        "score": 0,
        "submission_date": date.today().isoformat(),
    }
    submissions.append(submission)
    return submission


def cancel_submission(submissions: list[dict], submission_id: int) -> bool:
    """Отменить сдачу по ID. Вернуть True, если сдача найдена и удалена."""
    for i, s in enumerate(submissions):
        if s["id"] == submission_id:
            submissions.pop(i)
            return True
    return False


def get_statistics(submissions: list[dict]) -> dict:
    """Вернуть статистику по сдачам."""
    if not submissions:
        return {"total": 0, "submitted": 0, "average_score": 0.0}
    scores = [s["score"] for s in submissions if s["score"] > 0]
    return {
        "total": len(submissions),
        "submitted": len(scores),
        "average_score": sum(scores) / len(scores) if scores else 0.0,
    }