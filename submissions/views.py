"""Submission pages implemented with Django ORM querysets."""

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from submissions.models import Submission
from web_utils import paginate_queryset


def submission_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
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
    if status == "active":
        submissions = submissions.filter(is_cancelled=False)
    elif status == "cancelled":
        submissions = submissions.filter(is_cancelled=True)

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
