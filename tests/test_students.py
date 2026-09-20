"""Тесты класса Student и функций работы с коллекцией студентов."""

from models.students import (
    Student, add_student, find_student, get_student_by_id,
)


def test_student_creation():
    student = Student(1, "Васильчук Егор", "ЭФБО-02-24")
    assert student.id == 1
    assert student.name == "Васильчук Егор"
    assert student.group == "ЭФБО-02-24"


def test_student_str():
    student = Student(1, "Васильчук Егор", "ЭФБО-02-24")
    assert "Васильчук Егор" in str(student)


def test_student_from_data():
    student = Student.from_data({"id": 1, "name": "Иванов Иван", "group": "ЭФБО-02-24"})
    assert student.name == "Иванов Иван"


def test_add_student():
    students = []
    student = add_student(students, "Васильчук Егор", "ЭФБО-02-24")
    assert len(students) == 1
    assert student.id == 1
    assert students[0] is student


def test_find_student():
    students = []
    add_student(students, "Васильчук Егор", "ЭФБО-02-24")
    add_student(students, "Иванов Иван", "ЭФБО-02-24")
    found = find_student(students, "иван")
    assert len(found) == 1
    assert found[0].name == "Иванов Иван"


def test_get_student_by_id():
    students = []
    add_student(students, "Васильчук Егор", "ЭФБО-02-24")
    assert get_student_by_id(students, 1) is not None
    assert get_student_by_id(students, 99) is None