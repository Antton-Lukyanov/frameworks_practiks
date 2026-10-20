"""РўРµСЃС‚С‹ РєР»Р°СЃСЃР° Student Рё С„СѓРЅРєС†РёР№ СЂР°Р±РѕС‚С‹ СЃ РєРѕР»Р»РµРєС†РёРµР№ СЃС‚СѓРґРµРЅС‚РѕРІ."""

from models.students import (
    Student, add_student, find_student, get_student_by_id,
)


def test_student_creation():
    student = Student(1, "Р’Р°СЃРёР»СЊС‡СѓРє Р•РіРѕСЂ", "Р­Р¤Р‘Рћ-02-24")
    assert student.id == 1
    assert student.name == "Р’Р°СЃРёР»СЊС‡СѓРє Р•РіРѕСЂ"
    assert student.group == "Р­Р¤Р‘Рћ-02-24"


def test_student_str():
    student = Student(1, "Р’Р°СЃРёР»СЊС‡СѓРє Р•РіРѕСЂ", "Р­Р¤Р‘Рћ-02-24")
    assert "Р’Р°СЃРёР»СЊС‡СѓРє Р•РіРѕСЂ" in str(student)


def test_student_from_data():
    student = Student.from_data({"id": 1, "name": "РРІР°РЅРѕРІ РРІР°РЅ", "group": "Р­Р¤Р‘Рћ-02-24"})
    assert student.name == "РРІР°РЅРѕРІ РРІР°РЅ"


def test_add_student():
    students = []
    student = add_student(students, "Р’Р°СЃРёР»СЊС‡СѓРє Р•РіРѕСЂ", "Р­Р¤Р‘Рћ-02-24")
    assert len(students) == 1
    assert student.id == 1
    assert students[0] is student


def test_find_student():
    students = []
    add_student(students, "Р’Р°СЃРёР»СЊС‡СѓРє Р•РіРѕСЂ", "Р­Р¤Р‘Рћ-02-24")
    add_student(students, "РРІР°РЅРѕРІ РРІР°РЅ", "Р­Р¤Р‘Рћ-02-24")
    found = find_student(students, "РёРІР°РЅ")
    assert len(found) == 1
    assert found[0].name == "РРІР°РЅРѕРІ РРІР°РЅ"


def test_get_student_by_id():
    students = []
    add_student(students, "Р’Р°СЃРёР»СЊС‡СѓРє Р•РіРѕСЂ", "Р­Р¤Р‘Рћ-02-24")
    assert get_student_by_id(students, 1) is not None
    assert get_student_by_id(students, 99) is None

