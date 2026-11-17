"""Homepage and shared error page for the assignment service."""

from django.db.models import Avg, Count, Max, Min, Sum
from django.shortcuts import render

from students.models import Student
from submissions.models import Submission
from tasks.models import Task


def index(request):
    active_submissions = Submission.objects.filter(is_cancelled=False)
    scored_submissions = active_submissions.exclude(score=0)
    statistics = active_submissions.aggregate(
        total=Count("id"),
        total_score=Sum("score"),
    )
    statistics.update(
        scored_submissions.aggregate(
            average_score=Avg("score"),
            minimum_score=Min("score"),
            maximum_score=Max("score"),
        )
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
