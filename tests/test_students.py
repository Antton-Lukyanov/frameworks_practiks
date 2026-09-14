"""Тесты функций работы со студентами."""

from students import add_student, find_student, get_student_by_id


def test_add_student():
    students = []
    add_student(students, "Васильчук Егор", "ЭФБО-02-24")
    assert len(students) == 1
    assert students[0]["name"] == "Васильчук Егор"
    assert students[0]["id"] == 1


def test_find_student():
    students = []
    add_student(students, "Васильчук Егор", "ЭФБО-02-24")
    add_student(students, "Иванов Иван", "ЭФБО-02-24")
    found = find_student(students, "иван")
    assert len(found) == 1
    assert found[0]["name"] == "Иванов Иван"


def test_get_student_by_id():
    students = []
    add_student(students, "Васильчук Егор", "ЭФБО-02-24")
    assert get_student_by_id(students, 1) is not None
    assert get_student_by_id(students, 99) is None