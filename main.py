"""Точка запуска приложения «Сервис сдачи заданий»."""

from storage import (
    load_students, save_students,
    load_tasks, save_tasks,
    load_submissions, save_submissions,
)
from students import add_student, find_student
from tasks import add_task, find_task
from submissions import (
    create_submission, cancel_submission, get_statistics,
)
from utils import input_int, input_str, input_float


def show_students(students: list[dict]) -> None:
    """Вывести список студентов."""
    if not students:
        print("Список студентов пуст.")
        return
    print("\n--- Студенты ---")
    for s in students:
        print(f"[{s['id']}] {s['name']} (группа {s['group']})")


def show_tasks(tasks: list[dict]) -> None:
    """Вывести список заданий."""
    if not tasks:
        print("Список заданий пуст.")
        return
    print("\n--- Задания ---")
    for t in tasks:
        print(f"[{t['id']}] {t['title']} (макс. {t['max_score']} б., до {t['deadline']})")


def show_submissions(submissions: list[dict]) -> None:
    """Вывести список сдач."""
    if not submissions:
        print("Список сдач пуст.")
        return
    print("\n--- Сдачи ---")
    for s in submissions:
        print(f"[{s['id']}] студент {s['student_id']}, задание {s['task_id']}, "
              f"файл {s['file_name']} ({s['file_size_mb']} МБ), "
              f"балл {s['score']}, дата {s['submission_date']}")


def menu() -> None:
    """Вывести главное меню."""
    print("\n=== Сервис сдачи заданий ===")
    print("1. Показать студентов")
    print("2. Добавить студента")
    print("3. Найти студента")
    print("4. Показать задания")
    print("5. Добавить задание")
    print("6. Найти задание")
    print("7. Показать сдачи")
    print("8. Сдать задание")
    print("9. Отменить сдачу")
    print("10. Статистика")
    print("0. Выход")


def main() -> None:
    """Точка запуска: цикл меню и вызов функций проекта."""
    students = load_students("data/students.json")
    tasks = load_tasks("data/tasks.json")
    submissions = load_submissions("data/submissions.json")

    while True:
        menu()
        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_students(students)
        elif choice == 2:
            name = input_str("Имя студента: ")
            group = input_str("Группа: ")
            add_student(students, name, group)
            save_students("data/students.json", students)
            print("Студент добавлен.")
        elif choice == 3:
            query = input_str("Подстрока имени: ")
            show_students(find_student(students, query))
        elif choice == 4:
            show_tasks(tasks)
        elif choice == 5:
            title = input_str("Название задания: ")
            max_score = input_int("Максимальный балл: ")
            deadline = input_str("Дедлайн (ГГГГ-ММ-ДД): ")
            add_task(tasks, title, max_score, deadline)
            save_tasks("data/tasks.json", tasks)
            print("Задание добавлено.")
        elif choice == 6:
            query = input_str("Подстрока названия: ")
            show_tasks(find_task(tasks, query))
        elif choice == 7:
            show_submissions(submissions)
        elif choice == 8:
            student_id = input_int("ID студента: ")
            task_id = input_int("ID задания: ")
            file_name = input_str("Имя файла: ")
            file_size_mb = input_float("Размер файла (МБ): ")
            result = create_submission(
                submissions, student_id, task_id, file_name, file_size_mb
            )
            if result is None:
                print("Задание уже сдано этим студентом.")
            else:
                save_submissions("data/submissions.json", submissions)
                print("Сдача зафиксирована.")
        elif choice == 9:
            submission_id = input_int("ID сдачи: ")
            if cancel_submission(submissions, submission_id):
                save_submissions("data/submissions.json", submissions)
                print("Сдача отменена.")
            else:
                print("Сдача с таким ID не найдена.")
        elif choice == 10:
            stats = get_statistics(submissions)
            print(f"\nВсего сдач: {stats['total']}")
            print(f"Проверено: {stats['submitted']}")
            print(f"Средний балл: {stats['average_score']:.2f}")
        elif choice == 0:
            print("Выход из программы.")
            break
        else:
            print("Некорректный пункт меню.")


if __name__ == "__main__":
    main()