"""Student pages implemented with Django ORM querysets."""

from django.db.models import Avg, Count, Prefetch, Q
from django.shortcuts import get_object_or_404, render

from submissions.models import Submission
from students.models import Student
from web_utils import paginate_queryset


def student_list(request):
    query = request.GET.get("q", "").strip()
    group = request.GET.get("group", "").strip()
    ordering = request.GET.get("order", "name")
    orderings = {
        "name": "name",
        "name_desc": "-name",
        "group": "group",
        "group_desc": "-group",
        "submissions": "-submission_count",
        "score": "-average_score",
    }

    students = Student.objects.annotate(
        submission_count=Count(
            "submissions",
            filter=Q(submissions__is_cancelled=False),
        ),
        average_score=Avg(
            "submissions__score",
            filter=Q(
                submissions__is_cancelled=False,
                submissions__score__gt=0,
            ),
        ),
    )
    if query:
        students = students.filter(
            Q(name__icontains=query) | Q(group__icontains=query)
        )
    if group:
        students = students.filter(group=group)

    students = students.order_by(orderings.get(ordering, "name"), "id")
    page_obj, query_params = paginate_queryset(request, students)
    return render(
        request,
        "students/student_list.html",
        {
            "students": page_obj.object_list,
            "page_obj": page_obj,
            "query_params": query_params,
            "search_query": query,
            "selected_group": group,
            "selected_order": ordering,
            "groups": Student.objects.order_by("group")
            .values_list("group", flat=True)
            .distinct(),
        },
    )


def student_detail(request, student_id):
    submissions = Submission.objects.select_related("task")
    student = get_object_or_404(
        Student.objects.prefetch_related(
            Prefetch("submissions", queryset=submissions)
        ),
        pk=student_id,
    )
    return render(
        request,
        "students/student_detail.html",
        {"student": student, "submissions": student.submissions.all()},
    )
