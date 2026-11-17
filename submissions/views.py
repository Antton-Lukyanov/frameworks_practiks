"""Submission pages implemented with Django ORM querysets."""

from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date

from submissions.models import Submission
from students.models import Student
from tasks.models import Task
from web_utils import paginate_queryset


def submission_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    selected_date = request.GET.get("date", "").strip()
    task_id = request.GET.get("task", "").strip()
    student_id = request.GET.get("student", "").strip()
    ordering = request.GET.get("order", "date")
    orderings = {
        "date": "-submission_date",
        "date_asc": "submission_date",
        "score": "-score",
        "score_asc": "score",
        "student": "student__name",
        "task": "task__title",
    }

    submissions = Submission.objects.select_related("student", "task")
    if query:
        submissions = submissions.filter(
            Q(file_name__icontains=query)
            | Q(student__name__icontains=query)
            | Q(task__title__icontains=query)
        )
    status_filters = {
        Submission.Status.ACTIVE: submissions.active,
        Submission.Status.CANCELLED: submissions.cancelled,
        Submission.Status.COMPLETED: submissions.completed,
    }
    if status in status_filters:
        submissions = status_filters[status]()
    else:
        status = ""

    try:
        parsed_date = parse_date(selected_date)
    except ValueError:
        parsed_date = None
    if parsed_date:
        submissions = submissions.for_date(parsed_date)
    if task_id.isdecimal():
        submissions = submissions.filter(task_id=int(task_id))
    else:
        task_id = ""
    if student_id.isdecimal():
        submissions = submissions.filter(student_id=int(student_id))
    else:
        student_id = ""

    submissions = submissions.order_by(
        orderings.get(ordering, "-submission_date"), "-id"
    )
    page_obj, query_params = paginate_queryset(request, submissions)
    return render(
        request,
        "submissions/submission_list.html",
        {
            "submissions": page_obj.object_list,
            "page_obj": page_obj,
            "query_params": query_params,
            "search_query": query,
            "selected_status": status,
            "selected_order": ordering,
            "selected_date": selected_date,
            "selected_task": task_id,
            "selected_student": student_id,
            "tasks": Task.objects.order_by("title"),
            "students": Student.objects.order_by("name", "id"),
        },
    )


def submission_detail(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("student", "task"),
        pk=submission_id,
    )
    return render(
        request,
        "submissions/submission_detail.html",
        {"submission": submission},
    )
