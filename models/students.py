"""РљР»Р°СЃСЃ Student Рё С„СѓРЅРєС†РёРё СЂР°Р±РѕС‚С‹ СЃ РєРѕР»Р»РµРєС†РёРµР№ СЃС‚СѓРґРµРЅС‚РѕРІ."""

from __future__ import annotations


class Student:
    """РЎС‚СѓРґРµРЅС‚, СЃРґР°СЋС‰РёР№ СѓС‡РµР±РЅС‹Рµ Р·Р°РґР°РЅРёСЏ."""

    def __init__(self, student_id: int, name: str, group: str) -> None:
        """РЎРѕР·РґР°С‚СЊ РѕР±СЉРµРєС‚ СЃС‚СѓРґРµРЅС‚Р°."""
        self.id = student_id
        self.name = name
        self.group = group

    def __str__(self) -> str:
        """Р’РµСЂРЅСѓС‚СЊ СЃС‚СЂРѕРєРѕРІРѕРµ РїСЂРµРґСЃС‚Р°РІР»РµРЅРёРµ СЃС‚СѓРґРµРЅС‚Р°."""
        return f"[{self.id}] {self.name} (РіСЂСѓРїРїР° {self.group})"

    @classmethod
    def from_data(cls, data: dict) -> "Student":
        """РЎРѕР·РґР°С‚СЊ СЃС‚СѓРґРµРЅС‚Р° РёР· СЃР»РѕРІР°СЂСЏ (РґР°РЅРЅС‹Рµ РёР· JSON)."""
        return cls(
            student_id=data["id"],
            name=data["name"],
            group=data["group"],
        )

    def to_data(self) -> dict:
        """РџСЂРµРѕР±СЂР°Р·РѕРІР°С‚СЊ РѕР±СЉРµРєС‚ РІ СЃР»РѕРІР°СЂСЊ РґР»СЏ СЃРѕС…СЂР°РЅРµРЅРёСЏ РІ JSON."""
        return {"id": self.id, "name": self.name, "group": self.group}


def add_student(students: list[Student], name: str, group: str) -> Student:
    """РЎРѕР·РґР°С‚СЊ СЃС‚СѓРґРµРЅС‚Р° Рё РґРѕР±Р°РІРёС‚СЊ РµРіРѕ РІ РєРѕР»Р»РµРєС†РёСЋ. Р’РµСЂРЅСѓС‚СЊ РѕР±СЉРµРєС‚."""
    student_id = max((s.id for s in students), default=0) + 1
    student = Student(student_id, name, group)
    students.append(student)
    return student


def find_student(students: list[Student], query: str) -> list[Student]:
    """РќР°Р№С‚Рё СЃС‚СѓРґРµРЅС‚РѕРІ РїРѕ РїРѕРґСЃС‚СЂРѕРєРµ РёРјРµРЅРё (Р±РµР· СѓС‡С‘С‚Р° СЂРµРіРёСЃС‚СЂР°)."""
    query_lower = query.lower()
    return [s for s in students if query_lower in s.name.lower()]


def get_student_by_id(students: list[Student], student_id: int) -> Student | None:
    """Р’РµСЂРЅСѓС‚СЊ СЃС‚СѓРґРµРЅС‚Р° РїРѕ ID РёР»Рё None."""
    for s in students:
        if s.id == student_id:
            return s
    return None


def show_students(students: list[Student]) -> None:
    """Р’С‹РІРµСЃС‚Рё СЃРїРёСЃРѕРє СЃС‚СѓРґРµРЅС‚РѕРІ."""
    if not students:
        print("РЎРїРёСЃРѕРє СЃС‚СѓРґРµРЅС‚РѕРІ РїСѓСЃС‚.")
        return
    print("\n--- РЎС‚СѓРґРµРЅС‚С‹ ---")
    for s in students:
        print(s)

