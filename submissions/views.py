"""Submission pages implemented with Django ORM querysets."""

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SubmissionFilterForm, SubmissionForm
from submissions.models import Submission
from web_utils import paginate_queryset


def submission_list(request):
    filter_form = SubmissionFilterForm(request.GET)
    filters = filter_form.cleaned_data if filter_form.is_valid() else {}
    query = filters.get("q", "").strip()
    status = filters.get("status", "")
    ordering = filters.get("order") or "date"
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
            "filter_form": filter_form,
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


def submission_create(request):
    form = SubmissionForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        submission = form.save()
        messages.success(request, "Сдача задания создана.")
        return redirect("submissions:detail", submission_id=submission.pk)
    return render(
        request,
        "submissions/submission_form.html",
        {"form": form, "title": "Новая сдача", "submit_label": "Создать сдачу"},
    )


def submission_update(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    form = SubmissionForm(
        request.POST if request.method == "POST" else None,
        instance=submission,
    )
    if request.method == "POST" and form.is_valid():
        submission = form.save()
        messages.success(request, "Сдача задания обновлена.")
        return redirect("submissions:detail", submission_id=submission.pk)
    return render(
        request,
        "submissions/submission_form.html",
        {
            "form": form,
            "submission": submission,
            "title": f"Изменить сдачу №{submission.pk}",
            "submit_label": "Сохранить изменения",
        },
    )


@require_POST
def submission_cancel(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    if not submission.is_cancelled:
        submission.is_cancelled = True
        submission.save(update_fields=["is_cancelled"])
        messages.success(request, "Сдача отменена.")
    return redirect("submissions:detail", submission_id=submission.pk)
