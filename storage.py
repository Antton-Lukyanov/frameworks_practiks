"""РЎРѕС…СЂР°РЅРµРЅРёРµ Рё Р·Р°РіСЂСѓР·РєР° РґР°РЅРЅС‹С… РїСЂРѕРµРєС‚Р° РІ JSON-С„Р°Р№Р»Р°С….

РњРѕРґСѓР»СЊ СЂР°Р±РѕС‚Р°РµС‚ СЃ РєРѕР»Р»РµРєС†РёСЏРјРё РѕР±СЉРµРєС‚РѕРІ Student, Task, Submission.
РџСЂРё Р·Р°РіСЂСѓР·РєРµ JSON РїСЂРµРѕР±СЂР°Р·СѓРµС‚СЃСЏ РІ РѕР±СЉРµРєС‚С‹; РїСЂРё СЃРѕС…СЂР°РЅРµРЅРёРё вЂ” РѕР±СЂР°С‚РЅРѕ.
"""

from __future__ import annotations

import json
import os

from models.students import Student
from models.tasks import Task
from models.submissions import Submission


def _load_json(filename: str) -> list[dict]:
    """Р—Р°РіСЂСѓР·РёС‚СЊ СЃРїРёСЃРѕРє СЃР»РѕРІР°СЂРµР№ РёР· JSON-С„Р°Р№Р»Р°."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as error:
        print(f"РћС€РёР±РєР° С‡С‚РµРЅРёСЏ С„Р°Р№Р»Р° {filename}: {error}")
        return []


def _save_json(filename: str, data: list[dict]) -> None:
    """РЎРѕС…СЂР°РЅРёС‚СЊ СЃРїРёСЃРѕРє СЃР»РѕРІР°СЂРµР№ РІ JSON-С„Р°Р№Р»."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"РћС€РёР±РєР° Р·Р°РїРёСЃРё С„Р°Р№Р»Р° {filename}: {error}")


def load_students(filename: str) -> list[Student]:
    """Р—Р°РіСЂСѓР·РёС‚СЊ СЃС‚СѓРґРµРЅС‚РѕРІ РёР· JSON-С„Р°Р№Р»Р° РєР°Рє РѕР±СЉРµРєС‚С‹ Student."""
    return [Student.from_data(d) for d in _load_json(filename)]


def save_students(filename: str, students: list[Student]) -> None:
    """РЎРѕС…СЂР°РЅРёС‚СЊ РѕР±СЉРµРєС‚С‹ Student РІ JSON-С„Р°Р№Р»."""
    _save_json(filename, [s.to_data() for s in students])


def load_tasks(filename: str) -> list[Task]:
    """Р—Р°РіСЂСѓР·РёС‚СЊ Р·Р°РґР°РЅРёСЏ РёР· JSON-С„Р°Р№Р»Р° РєР°Рє РѕР±СЉРµРєС‚С‹ Task."""
    return [Task.from_data(d) for d in _load_json(filename)]


def save_tasks(filename: str, tasks: list[Task]) -> None:
    """РЎРѕС…СЂР°РЅРёС‚СЊ РѕР±СЉРµРєС‚С‹ Task РІ JSON-С„Р°Р№Р»."""
    _save_json(filename, [t.to_data() for t in tasks])


def load_submissions(
    filename: str,
    students: list[Student],
    tasks: list[Task],
) -> list[Submission]:
    """Р—Р°РіСЂСѓР·РёС‚СЊ СЃРґР°С‡Рё РёР· JSON-С„Р°Р№Р»Р° РєР°Рє РѕР±СЉРµРєС‚С‹ Submission.

    Р”Р»СЏ РІРѕСЃСЃС‚Р°РЅРѕРІР»РµРЅРёСЏ СЃРІСЏР·РµР№ РѕР±СЉРµРєС‚ Submission С‚СЂРµР±СѓРµС‚ РєРѕР»Р»РµРєС†РёРё
    СЃС‚СѓРґРµРЅС‚РѕРІ Рё Р·Р°РґР°РЅРёР№.
    """
    submissions: list[Submission] = []
    for d in _load_json(filename):
        submission = Submission.from_data(d, students, tasks)
        if submission is not None:
            submissions.append(submission)
    return submissions


def save_submissions(filename: str, submissions: list[Submission]) -> None:
    """РЎРѕС…СЂР°РЅРёС‚СЊ РѕР±СЉРµРєС‚С‹ Submission РІ JSON-С„Р°Р№Р»."""
    _save_json(filename, [s.to_data() for s in submissions])

