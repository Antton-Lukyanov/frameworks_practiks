"""Функции для работы со студентами."""


def add_student(students: list[dict], name: str, group: str) -> None:
    """Добавить студента в список students."""
    student_id = max((s["id"] for s in students), default=0) + 1
    students.append({"id": student_id, "name": name, "group": group})


def find_student(students: list[dict], query: str) -> list[dict]:
    """Найти студентов по подстроке имени (без учёта регистра)."""
    query_lower = query.lower()
    return [s for s in students if query_lower in s["name"].lower()]


def get_student_by_id(students: list[dict], student_id: int) -> dict | None:
    """Вернуть студента по ID или None."""
    for s in students:
        if s["id"] == student_id:
            return s
    return None