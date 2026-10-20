"""РљР»Р°СЃСЃ Submission Рё С„СѓРЅРєС†РёРё СЂР°Р±РѕС‚С‹ СЃ РєРѕР»Р»РµРєС†РёРµР№ СЃРґР°С‡.

Р¤СѓРЅРєС†РёРё get_task_status(), check_file_size() Рё get_result()
РїРµСЂРµРЅРµСЃРµРЅС‹ РёР· РџР 1/РџР 2 Рё РѕСЃС‚Р°СЋС‚СЃСЏ РѕР±С‹С‡РЅС‹РјРё С„СѓРЅРєС†РёСЏРјРё:
РѕРЅРё РЅРµ РѕС‚РЅРѕСЃСЏС‚СЃСЏ Рє СЃРѕСЃС‚РѕСЏРЅРёСЋ РєРѕРЅРєСЂРµС‚РЅРѕРіРѕ РѕР±СЉРµРєС‚Р°.
"""

from __future__ import annotations

from datetime import date

from .students import Student
from .tasks import Task


class Submission:
    """Р¤Р°РєС‚ СЃРґР°С‡Рё Р·Р°РґР°РЅРёСЏ СЃС‚СѓРґРµРЅС‚РѕРј."""

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
        """РЎРѕР·РґР°С‚СЊ РѕР±СЉРµРєС‚ СЃРґР°С‡Рё."""
        self.id = submission_id
        self.student = student
        self.task = task
        self.file_name = file_name
        self.file_size_mb = file_size_mb
        self.score = score
        self.submission_date = submission_date or date.today().isoformat()
        self.is_cancelled = False

    def __str__(self) -> str:
        """Р’РµСЂРЅСѓС‚СЊ СЃС‚СЂРѕРєРѕРІРѕРµ РїСЂРµРґСЃС‚Р°РІР»РµРЅРёРµ СЃРґР°С‡Рё."""
        status = "РѕС‚РјРµРЅРµРЅР°" if self.is_cancelled else "Р°РєС‚РёРІРЅР°"
        return (
            f"[{self.id}] {self.student.name} в†’ {self.task.title}, "
            f"С„Р°Р№Р» {self.file_name} ({self.file_size_mb} РњР‘), "
            f"Р±Р°Р»Р» {self.score}, РґР°С‚Р° {self.submission_date}, {status}"
        )

    def cancel(self) -> None:
        """РћС‚РјРµРЅРёС‚СЊ СЃРґР°С‡Сѓ, РёР·РјРµРЅРёРІ РµС‘ СЃРѕСЃС‚РѕСЏРЅРёРµ."""
        self.is_cancelled = True

    def get_result(self) -> str:
        """Р’РµСЂРЅСѓС‚СЊ С‚РµРєСЃС‚РѕРІС‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚ РїРѕ Р±Р°Р»Р»Р°Рј."""
        return get_result(self.score)

    def to_data(self) -> dict:
        """РџСЂРµРѕР±СЂР°Р·РѕРІР°С‚СЊ РѕР±СЉРµРєС‚ РІ СЃР»РѕРІР°СЂСЊ РґР»СЏ СЃРѕС…СЂР°РЅРµРЅРёСЏ РІ JSON."""
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
        """РЎРѕР·РґР°С‚СЊ СЃРґР°С‡Сѓ РёР· СЃР»РѕРІР°СЂСЏ, РЅР°Р№РґСЏ СЃРІСЏР·Р°РЅРЅС‹Рµ РѕР±СЉРµРєС‚С‹ Student Рё Task."""
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


# ---------- Р¤СѓРЅРєС†РёРё, РїРµСЂРµРЅРµСЃС‘РЅРЅС‹Рµ РёР· РџР 1 (РЅРµ РјРµС‚РѕРґС‹) ----------

def get_task_status(is_submitted: bool) -> str:
    """Р’РµСЂРЅСѓС‚СЊ С‚РµРєСЃС‚РѕРІС‹Р№ СЃС‚Р°С‚СѓСЃ СЃРґР°С‡Рё Р·Р°РґР°РЅРёСЏ."""
    if is_submitted:
        return "Р—Р°РґР°РЅРёРµ СЃРґР°РЅРѕ"
    return "Р—Р°РґР°РЅРёРµ РЅРµ СЃРґР°РЅРѕ"


def check_file_size(file_size_mb: float) -> str:
    """РџСЂРѕРІРµСЂРёС‚СЊ РґРѕРїСѓСЃС‚РёРјС‹Р№ СЂР°Р·РјРµСЂ С„Р°Р№Р»Р° (РјР°РєСЃ. 10 РњР‘)."""
    if file_size_mb > 10:
        return "Р¤Р°Р№Р» СЃР»РёС€РєРѕРј Р±РѕР»СЊС€РѕР№ (РјР°РєСЃ. 10 РњР‘)"
    return "Р¤Р°Р№Р» РґРѕРїСѓСЃС‚РёРјРѕРіРѕ СЂР°Р·РјРµСЂР°"


def get_result(score: int) -> str:
    """Р’С‹СЃС‚Р°РІРёС‚СЊ СЂРµР·СѓР»СЊС‚Р°С‚ РїРѕ Р±Р°Р»Р»Р°Рј."""
    if score >= 80:
        return "РћС‚Р»РёС‡РЅРѕ"
    elif score >= 60:
        return "РҐРѕСЂРѕС€Рѕ"
    else:
        return "РўСЂРµР±СѓРµС‚СЃСЏ РґРѕСЂР°Р±РѕС‚РєР°"


# ---------- Р¤СѓРЅРєС†РёРё СЂР°Р±РѕС‚С‹ СЃ РєРѕР»Р»РµРєС†РёРµР№ РѕР±СЉРµРєС‚РѕРІ Submission ----------

def is_task_submitted(submissions: list[Submission], student: Student, task: Task) -> bool:
    """РџСЂРѕРІРµСЂРёС‚СЊ, СЃРґР°РЅРѕ Р»Рё Р·Р°РґР°РЅРёРµ СЃС‚СѓРґРµРЅС‚РѕРј (СѓС‡РёС‚С‹РІР°СЋС‚СЃСЏ С‚РѕР»СЊРєРѕ Р°РєС‚РёРІРЅС‹Рµ СЃРґР°С‡Рё)."""
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
    """РЎРѕР·РґР°С‚СЊ РЅРѕРІСѓСЋ СЃРґР°С‡Сѓ. Р’РµСЂРЅСѓС‚СЊ None, РµСЃР»Рё Р·Р°РґР°РЅРёРµ СѓР¶Рµ СЃРґР°РЅРѕ."""
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
    """РћС‚РјРµРЅРёС‚СЊ СЃРґР°С‡Сѓ РїРѕ ID. Р’РµСЂРЅСѓС‚СЊ True, РµСЃР»Рё СЃРґР°С‡Р° РЅР°Р№РґРµРЅР°."""
    for s in submissions:
        if s.id == submission_id:
            s.cancel()
            return True
    return False


def get_statistics(submissions: list[Submission]) -> dict:
    """Р’РµСЂРЅСѓС‚СЊ СЃС‚Р°С‚РёСЃС‚РёРєСѓ РїРѕ СЃРґР°С‡Р°Рј."""
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
    """Р’С‹РІРµСЃС‚Рё СЃРїРёСЃРѕРє СЃРґР°С‡."""
    if not submissions:
        print("РЎРїРёСЃРѕРє СЃРґР°С‡ РїСѓСЃС‚.")
        return
    print("\n--- РЎРґР°С‡Рё ---")
    for s in submissions:
        print(s)

