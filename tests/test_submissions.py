"""Тесты функций работы со сдачами."""

from submissions import (
    is_task_submitted,
    create_submission,
    cancel_submission,
    get_result,
    check_file_size,
    get_statistics,
)


def test_is_task_submitted_false():
    submissions = []
    assert not is_task_submitted(submissions, 1, 1)


def test_duplicate_submission_forbidden():
    submissions = []
    create_submission(submissions, 1, 1, "report.pdf", 5.0)
    assert is_task_submitted(submissions, 1, 1)
    second = create_submission(submissions, 1, 1, "report2.pdf", 3.0)
    assert second is None


def test_cancel_submission():
    submissions = []
    create_submission(submissions, 1, 1, "report.pdf", 5.0)
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
    create_submission(submissions, 1, 1, "a.pdf", 5.0)
    submissions[0]["score"] = 80
    stats = get_statistics(submissions)
    assert stats["total"] == 1
    assert stats["submitted"] == 1
    assert stats["average_score"] == 80.0