"""Homepage and shared error page for the assignment service."""

from django.db.models import Avg, Count, Max, Min, Q, Sum
from django.shortcuts import render

from students.models import Student
from submissions.models import Submission
from tasks.models import Task


def index(request):
    statistics = Submission.objects.aggregate(
        total=Count("id"),
        active=Count("id", filter=Q(status=Submission.Status.ACTIVE)),
        cancelled=Count("id", filter=Q(status=Submission.Status.CANCELLED)),
        completed=Count("id", filter=Q(status=Submission.Status.COMPLETED)),
        passing=Count(
            "id",
            filter=Q(
                status=Submission.Status.COMPLETED,
                is_passing=True,
            ),
        ),
        total_score=Sum(
            "score",
            filter=Q(status=Submission.Status.COMPLETED),
        ),
        average_score=Avg(
            "score",
            filter=Q(status=Submission.Status.COMPLETED),
        ),
        minimum_score=Min(
            "score",
            filter=Q(status=Submission.Status.COMPLETED),
        ),
        maximum_score=Max(
            "score",
            filter=Q(status=Submission.Status.COMPLETED),
        ),
    )
    return render(
        request,
        "homepage/index.html",
        {
            "student_count": Student.objects.count(),
            "task_count": Task.objects.count(),
            "statistics": statistics,
        },
    )


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
