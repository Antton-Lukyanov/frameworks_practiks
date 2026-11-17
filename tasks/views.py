"""Task pages implemented with Django ORM querysets."""

from django.db.models import Avg, Count, Prefetch, Q
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date

from submissions.models import Submission
from tasks.models import Task
from web_utils import paginate_queryset


def task_list(request):
    query = request.GET.get("q", "").strip()
    deadline_from = request.GET.get("deadline_from", "").strip()
    deadline_to = request.GET.get("deadline_to", "").strip()
    ordering = request.GET.get("order", "deadline")
    orderings = {
        "deadline": "deadline",
        "deadline_desc": "-deadline",
        "title": "title",
        "title_desc": "-title",
        "submissions": "-submission_count",
        "score": "-average_score",
    }

    tasks = Task.objects.annotate(
        submission_count=Count(
            "submissions",
            filter=Q(
                submissions__status__in=(
                    Submission.Status.ACTIVE,
                    Submission.Status.COMPLETED,
                )
            ),
        ),
        average_score=Avg(
            "submissions__score",
            filter=Q(
                submissions__status=Submission.Status.COMPLETED,
                submissions__score__gt=0,
            ),
        ),
    )
    if query:
        tasks = tasks.filter(title__icontains=query)
    try:
        parsed_from = parse_date(deadline_from)
    except ValueError:
        parsed_from = None
    try:
        parsed_to = parse_date(deadline_to)
    except ValueError:
        parsed_to = None
    if parsed_from:
        tasks = tasks.filter(deadline__gte=parsed_from)
    if parsed_to:
        tasks = tasks.filter(deadline__lte=parsed_to)

    tasks = tasks.order_by(orderings.get(ordering, "deadline"), "id")
    page_obj, query_params = paginate_queryset(request, tasks)
    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": page_obj.object_list,
            "page_obj": page_obj,
            "query_params": query_params,
            "search_query": query,
            "deadline_from": deadline_from,
            "deadline_to": deadline_to,
            "selected_order": ordering,
        },
    )


def task_detail(request, slug):
    submissions = Submission.objects.select_related("student")
    task = get_object_or_404(
        Task.objects.prefetch_related(
            Prefetch("submissions", queryset=submissions)
        ),
        **({"pk": int(slug)} if slug.isdecimal() else {"slug": slug}),
    )
    return render(
        request,
        "tasks/task_detail.html",
        {"task": task, "submissions": task.submissions.all()},
    )
