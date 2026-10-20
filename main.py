"""РўРѕС‡РєР° Р·Р°РїСѓСЃРєР° РїСЂРёР»РѕР¶РµРЅРёСЏ В«РЎРµСЂРІРёСЃ СЃРґР°С‡Рё Р·Р°РґР°РЅРёР№В»."""

from __future__ import annotations

from storage import (
    load_students, save_students,
    load_tasks, save_tasks,
    load_submissions, save_submissions,
)
from models.students import (
    Student, add_student, find_student, get_student_by_id, show_students,
)
from models.tasks import (
    Task, add_task, find_task, get_task_by_id, show_tasks,
)
from models.submissions import (
    Submission, create_submission, cancel_submission,
    get_statistics, show_submissions,
)
from utils import input_int, input_str, input_float


def menu() -> None:
    """Р’С‹РІРµСЃС‚Рё РіР»Р°РІРЅРѕРµ РјРµРЅСЋ."""
    print("\n=== РЎРµСЂРІРёСЃ СЃРґР°С‡Рё Р·Р°РґР°РЅРёР№ ===")
    print("1. РџРѕРєР°Р·Р°С‚СЊ СЃС‚СѓРґРµРЅС‚РѕРІ")
    print("2. Р”РѕР±Р°РІРёС‚СЊ СЃС‚СѓРґРµРЅС‚Р°")
    print("3. РќР°Р№С‚Рё СЃС‚СѓРґРµРЅС‚Р°")
    print("4. РџРѕРєР°Р·Р°С‚СЊ Р·Р°РґР°РЅРёСЏ")
    print("5. Р”РѕР±Р°РІРёС‚СЊ Р·Р°РґР°РЅРёРµ")
    print("6. РќР°Р№С‚Рё Р·Р°РґР°РЅРёРµ")
    print("7. РџРѕРєР°Р·Р°С‚СЊ СЃРґР°С‡Рё")
    print("8. РЎРґР°С‚СЊ Р·Р°РґР°РЅРёРµ")
    print("9. РћС‚РјРµРЅРёС‚СЊ СЃРґР°С‡Сѓ")
    print("10. РЎС‚Р°С‚РёСЃС‚РёРєР°")
    print("0. Р’С‹С…РѕРґ")


def create_new_submission(
    submissions: list[Submission],
    students: list[Student],
    tasks: list[Task],
) -> None:
    """РЎС†РµРЅР°СЂРёР№ СЃРґР°С‡Рё Р·Р°РґР°РЅРёСЏ: РїРѕРёСЃРє СЃС‚СѓРґРµРЅС‚Р° Рё Р·Р°РґР°РЅРёСЏ, СЃРѕР·РґР°РЅРёРµ РѕР±СЉРµРєС‚Р° Submission."""
    student_id = input_int("ID СЃС‚СѓРґРµРЅС‚Р°: ")
    student = get_student_by_id(students, student_id)
    if student is None:
        print("РЎС‚СѓРґРµРЅС‚ СЃ С‚Р°РєРёРј ID РЅРµ РЅР°Р№РґРµРЅ.")
        return

    task_id = input_int("ID Р·Р°РґР°РЅРёСЏ: ")
    task = get_task_by_id(tasks, task_id)
    if task is None:
        print("Р—Р°РґР°РЅРёРµ СЃ С‚Р°РєРёРј ID РЅРµ РЅР°Р№РґРµРЅРѕ.")
        return

    file_name = input_str("РРјСЏ С„Р°Р№Р»Р°: ")
    file_size_mb = input_float("Р Р°Р·РјРµСЂ С„Р°Р№Р»Р° (РњР‘): ")

    submission = create_submission(submissions, student, task, file_name, file_size_mb)
    if submission is None:
        print("Р—Р°РґР°РЅРёРµ СѓР¶Рµ СЃРґР°РЅРѕ СЌС‚РёРј СЃС‚СѓРґРµРЅС‚РѕРј.")
    else:
        print(f"РЎРґР°С‡Р° Р·Р°С„РёРєСЃРёСЂРѕРІР°РЅР°. ID = {submission.id}")


def main() -> None:
    """РўРѕС‡РєР° Р·Р°РїСѓСЃРєР°: С†РёРєР» РјРµРЅСЋ Рё РІС‹Р·РѕРІ С„СѓРЅРєС†РёР№ РїСЂРѕРµРєС‚Р°."""
    students = load_students("data/students.json")
    tasks = load_tasks("data/tasks.json")
    submissions = load_submissions("data/submissions.json", students, tasks)

    while True:
        menu()
        choice = input_int("Р’С‹Р±РµСЂРёС‚Рµ РґРµР№СЃС‚РІРёРµ: ")

        if choice == 1:
            show_students(students)
        elif choice == 2:
            name = input_str("РРјСЏ СЃС‚СѓРґРµРЅС‚Р°: ")
            group = input_str("Р“СЂСѓРїРїР°: ")
            add_student(students, name, group)
            save_students("data/students.json", students)
            print("РЎС‚СѓРґРµРЅС‚ РґРѕР±Р°РІР»РµРЅ.")
        elif choice == 3:
            query = input_str("РџРѕРґСЃС‚СЂРѕРєР° РёРјРµРЅРё: ")
            show_students(find_student(students, query))
        elif choice == 4:
            show_tasks(tasks)
        elif choice == 5:
            title = input_str("РќР°Р·РІР°РЅРёРµ Р·Р°РґР°РЅРёСЏ: ")
            max_score = input_int("РњР°РєСЃРёРјР°Р»СЊРЅС‹Р№ Р±Р°Р»Р»: ")
            deadline = input_str("Р”РµРґР»Р°Р№РЅ (Р“Р“Р“Р“-РњРњ-Р”Р”): ")
            add_task(tasks, title, max_score, deadline)
            save_tasks("data/tasks.json", tasks)
            print("Р—Р°РґР°РЅРёРµ РґРѕР±Р°РІР»РµРЅРѕ.")
        elif choice == 6:
            query = input_str("РџРѕРґСЃС‚СЂРѕРєР° РЅР°Р·РІР°РЅРёСЏ: ")
            show_tasks(find_task(tasks, query))
        elif choice == 7:
            show_submissions(submissions)
        elif choice == 8:
            create_new_submission(submissions, students, tasks)
            save_submissions("data/submissions.json", submissions)
        elif choice == 9:
            submission_id = input_int("ID СЃРґР°С‡Рё: ")
            if cancel_submission(submissions, submission_id):
                save_submissions("data/submissions.json", submissions)
                print("РЎРґР°С‡Р° РѕС‚РјРµРЅРµРЅР°.")
            else:
                print("РЎРґР°С‡Р° СЃ С‚Р°РєРёРј ID РЅРµ РЅР°Р№РґРµРЅР°.")
        elif choice == 10:
            stats = get_statistics(submissions)
            print(f"\nР’СЃРµРіРѕ СЃРґР°С‡: {stats['total']}")
            print(f"РџСЂРѕРІРµСЂРµРЅРѕ: {stats['submitted']}")
            print(f"РЎСЂРµРґРЅРёР№ Р±Р°Р»Р»: {stats['average_score']:.2f}")
        elif choice == 0:
            print("Р’С‹С…РѕРґ РёР· РїСЂРѕРіСЂР°РјРјС‹.")
            break
        else:
            print("РќРµРєРѕСЂСЂРµРєС‚РЅС‹Р№ РїСѓРЅРєС‚ РјРµРЅСЋ.")


if __name__ == "__main__":
    main()

