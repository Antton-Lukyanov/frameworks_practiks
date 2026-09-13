
from datetime import date

#Возврат статуса сдачи задания
def get_task_status(is_submitted):

    if is_submitted:
        return "Задание сдано"
    return "Задание не сдано"

#Проверка допустимого размера файла (макс. 10 МБ)
def check_file_size(file_size_mb):

    if file_size_mb > 10:
        return "Файл слишком большой (макс. 10 МБ)"
    return "Файл допустимого размера"

#Выставление результата по баллам
def get_result(score):

    if score >= 80:
        return "Отлично"
    elif score >= 60:
        return "Хорошо"
    else:
        return "Требуется доработка"


def main():

    student_name = "Васильчук Егор"
    task_title = "Практическая работа №1"
    file_name = "report.pdf"
    file_size_mb = 6.7
    is_submitted = True
    score = 87
    submission_date = date(2026, 8, 23)

    print(f"Студент: {student_name}")
    print(f"Задание: {task_title}")
    print(f"Файл: {file_name} ({file_size_mb} МБ)")
    print(f"Дата сдачи: {submission_date}")
    print(get_task_status(is_submitted))
    print(check_file_size(file_size_mb))
    print(f"Результат: {get_result(score)}")


if __name__ == "__main__":
    main()