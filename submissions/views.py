"""Submission list and detail pages backed by SQLite joins."""

from django.shortcuts import render

from db.queries import fetch_submission, fetch_submissions
from models.students import Student
from models.submissions import Submission
from models.tasks import Task


def _to_submission(row):
    student = Student(row["student_id"], row["student_name"], row["student_group"])
    task = Task(
        row["task_id"],
        row["task_title"],
        row["max_score"],
        row["deadline"],
    )
    submission = Submission(
        row["id"],
        student,
        task,
        row["file_name"],
        row["file_size_mb"],
        row["score"],
        row["submission_date"],
    )
    submission.is_cancelled = bool(row["is_cancelled"])
    return submission


def submission_list(request):
    submissions = [_to_submission(row) for row in fetch_submissions()]
    return render(
        request,
        "submissions/submission_list.html",
        {"submissions": submissions},
    )


def submission_detail(request, submission_id):
    row = fetch_submission(submission_id)
    submission = _to_submission(row) if row is not None else None
    return render(
        request,
        "submissions/submission_detail.html",
        {"submission": submission},
        status=404 if submission is None else 200,
    )
