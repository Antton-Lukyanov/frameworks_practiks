"""РљР»Р°СЃСЃ Task Рё С„СѓРЅРєС†РёРё СЂР°Р±РѕС‚С‹ СЃ РєРѕР»Р»РµРєС†РёРµР№ Р·Р°РґР°РЅРёР№."""

from __future__ import annotations

from datetime import date


class Task:
    """РЈС‡РµР±РЅРѕРµ Р·Р°РґР°РЅРёРµ."""

    def __init__(self, task_id: int, title: str, max_score: int, deadline: str) -> None:
        """РЎРѕР·РґР°С‚СЊ РѕР±СЉРµРєС‚ Р·Р°РґР°РЅРёСЏ."""
        self.id = task_id
        self.title = title
        self.max_score = max_score
        self.deadline = deadline

    def __str__(self) -> str:
        """Р’РµСЂРЅСѓС‚СЊ СЃС‚СЂРѕРєРѕРІРѕРµ РїСЂРµРґСЃС‚Р°РІР»РµРЅРёРµ Р·Р°РґР°РЅРёСЏ."""
        return f"[{self.id}] {self.title} (РјР°РєСЃ. {self.max_score} Р±., РґРѕ {self.deadline})"

    def is_expired(self, current_date: str) -> bool:
        """РџСЂРѕРІРµСЂРёС‚СЊ, РёСЃС‚С‘Рє Р»Рё СЃСЂРѕРє СЃРґР°С‡Рё Р·Р°РґР°РЅРёСЏ."""
        return date.fromisoformat(current_date) > date.fromisoformat(self.deadline)

    @classmethod
    def from_data(cls, data: dict) -> "Task":
        """РЎРѕР·РґР°С‚СЊ Р·Р°РґР°РЅРёРµ РёР· СЃР»РѕРІР°СЂСЏ (РґР°РЅРЅС‹Рµ РёР· JSON)."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            max_score=data["max_score"],
            deadline=data["deadline"],
        )

    def to_data(self) -> dict:
        """РџСЂРµРѕР±СЂР°Р·РѕРІР°С‚СЊ РѕР±СЉРµРєС‚ РІ СЃР»РѕРІР°СЂСЊ РґР»СЏ СЃРѕС…СЂР°РЅРµРЅРёСЏ РІ JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "max_score": self.max_score,
            "deadline": self.deadline,
        }


def add_task(tasks: list[Task], title: str, max_score: int, deadline: str) -> Task:
    """РЎРѕР·РґР°С‚СЊ Р·Р°РґР°РЅРёРµ Рё РґРѕР±Р°РІРёС‚СЊ РµРіРѕ РІ РєРѕР»Р»РµРєС†РёСЋ. Р’РµСЂРЅСѓС‚СЊ РѕР±СЉРµРєС‚."""
    task_id = max((t.id for t in tasks), default=0) + 1
    task = Task(task_id, title, max_score, deadline)
    tasks.append(task)
    return task


def find_task(tasks: list[Task], query: str) -> list[Task]:
    """РќР°Р№С‚Рё Р·Р°РґР°РЅРёСЏ РїРѕ РїРѕРґСЃС‚СЂРѕРєРµ РЅР°Р·РІР°РЅРёСЏ (Р±РµР· СѓС‡С‘С‚Р° СЂРµРіРёСЃС‚СЂР°)."""
    query_lower = query.lower()
    return [t for t in tasks if query_lower in t.title.lower()]


def get_task_by_id(tasks: list[Task], task_id: int) -> Task | None:
    """Р’РµСЂРЅСѓС‚СЊ Р·Р°РґР°РЅРёРµ РїРѕ ID РёР»Рё None."""
    for t in tasks:
        if t.id == task_id:
            return t
    return None


def filter_tasks_by_deadline(tasks: list[Task], deadline: str) -> list[Task]:
    """РћС‚РѕР±СЂР°С‚СЊ Р·Р°РґР°РЅРёСЏ СЃ РґРµРґР»Р°Р№РЅРѕРј РЅРµ РїРѕР·Р¶Рµ СѓРєР°Р·Р°РЅРЅРѕР№ РґР°С‚С‹."""
    limit = date.fromisoformat(deadline)
    return [t for t in tasks if date.fromisoformat(t.deadline) <= limit]


def show_tasks(tasks: list[Task]) -> None:
    """Р’С‹РІРµСЃС‚Рё СЃРїРёСЃРѕРє Р·Р°РґР°РЅРёР№."""
    if not tasks:
        print("РЎРїРёСЃРѕРє Р·Р°РґР°РЅРёР№ РїСѓСЃС‚.")
        return
    print("\n--- Р—Р°РґР°РЅРёСЏ ---")
    for t in tasks:
        print(t)

