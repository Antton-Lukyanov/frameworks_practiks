"""Класс Student и функции работы с коллекцией студентов."""

from __future__ import annotations


class Student:
    """Студент, сдающий учебные задания."""

    def __init__(self, student_id: int, name: str, group: str) -> None:
        """Создать объект студента."""
        self.id = student_id
        self.name = name
        self.group = group

    def __str__(self) -> str:
        """Вернуть строковое представление студента."""
        return f"[{self.id}] {self.name} (группа {self.group})"

    @classmethod
    def from_data(cls, data: dict) -> "Student":
        """Создать студента из словаря (данные из JSON)."""
        return cls(
            student_id=data["id"],
            name=data["name"],
            group=data["group"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для сохранения в JSON."""
        return {"id": self.id, "name": self.name, "group": self.group}


def add_student(students: list[Student], name: str, group: str) -> Student:
    """Создать студента и добавить его в коллекцию. Вернуть объект."""
    student_id = max((s.id for s in students), default=0) + 1
    student = Student(student_id, name, group)
    students.append(student)
    return student


def find_student(students: list[Student], query: str) -> list[Student]:
    """Найти студентов по подстроке имени (без учёта регистра)."""
    query_lower = query.lower()
    return [s for s in students if query_lower in s.name.lower()]


def get_student_by_id(students: list[Student], student_id: int) -> Student | None:
    """Вернуть студента по ID или None."""
    for s in students:
        if s.id == student_id:
            return s
    return None


def show_students(students: list[Student]) -> None:
    """Вывести список студентов."""
    if not students:
        print("Список студентов пуст.")
        return
    print("\n--- Студенты ---")
    for s in students:
        print(s)