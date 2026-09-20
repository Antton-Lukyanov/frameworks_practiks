"""Тесты класса Submission и функций работы со сдачами."""

from models.students import Student
from models.tasks import Task
from models.submissions import (
    Submission,
    is_task_submitted,
    create_submission,
    cancel_submission,
    get_result,
    check_file_size,
    get_statistics,
)


def _make_student() -> Student:
    return Student(1, "Васильчук Егор", "ЭФБО-02-24")


def _make_task() -> Task:
    return Task(1, "Практическая работа №1", 100, "2026-09-15")


def test_submission_creation():
    student = _make_student()
    task = _make_task()
    submission = Submission(1, student, task, "report.pdf", 5.0)
    assert submission.id == 1
    assert submission.student is student
    assert submission.task is task
    assert submission.file_name == "report.pdf"
    assert not submission.is_cancelled


def test_submission_cancel():
    submission = Submission(1, _make_student(), _make_task(), "report.pdf", 5.0)
    submission.cancel()
    assert submission.is_cancelled


def test_is_task_submitted_false():
    submissions = []
    assert not is_task_submitted(submissions, _make_student(), _make_task())


def test_duplicate_submission_forbidden():
    submissions = []
    student = _make_student()
    task = _make_task()
    create_submission(submissions, student, task, "report.pdf", 5.0)
    assert is_task_submitted(submissions, student, task)
    second = create_submission(submissions, student, task, "report2.pdf", 3.0)
    assert second is None


def test_cancel_submission():
    submissions = []
    create_submission(submissions, _make_student(), _make_task(), "report.pdf", 5.0)
    assert cancel_submission(submissions, 1)
    assert not cancel_submission(submissions, 99)


def test_get_result():
    assert get_result(90) == "Отлично"
    assert get_result(70) == "Хорошо"
    assert get_result(50) == "Требуется доработка"


def test_check_file_size():
    assert check_file_size(5.0) == "Файл допустимого размера"
    assert check_file_size(15.0) == "Файл слишком большой (макс. 10 МБ)"


def test_get_statistics():
    submissions = []
    create_submission(submissions, _make_student(), _make_task(), "a.pdf", 5.0)
    submissions[0].score = 80
    stats = get_statistics(submissions)
    assert stats["total"] == 1
    assert stats["submitted"] == 1
    assert stats["average_score"] == 80.0