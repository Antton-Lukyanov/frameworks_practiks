from datetime import date

import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.test import Client
from django.urls import reverse

from students.admin import StudentAdmin
from students.models import Student
from submissions.admin import SubmissionAdmin
from submissions.models import Submission
from tasks.admin import TaskAdmin
from tasks.models import Task


@pytest.fixture
def student(db):
    return Student.objects.create(name="Иван Иванов", group="ЭФБО-02-24")


@pytest.fixture
def task(db):
    return Task.objects.create(
        title="Практическая работа", max_score=100, deadline=date(2026, 12, 1)
    )


def make_submission(student, task, status, *, day=date(2026, 11, 1), score=0):
    return Submission.objects.create(
        student=student,
        task=task,
        file_name=f"{status}.pdf",
        file_size_mb=1,
        score=score,
        submission_date=day,
        status=status,
    )


@pytest.mark.django_db
def test_submission_queryset_status_and_date_methods(student, task):
    active = make_submission(student, task, Submission.Status.ACTIVE)
    cancelled = make_submission(
        student, task, Submission.Status.CANCELLED, day=date(2026, 11, 2)
    )
    completed = make_submission(
        student, task, Submission.Status.COMPLETED, day=date(2026, 11, 3)
    )

    scoped = Submission.objects.filter(student=student, task=task)
    assert list(scoped.active()) == [active]
    assert list(scoped.cancelled()) == [cancelled]
    assert list(scoped.completed()) == [completed]
    assert list(scoped.for_date(date(2026, 11, 2))) == [cancelled]
    assert list(scoped.not_cancelled()) == [completed, active]


@pytest.mark.django_db
def test_only_one_active_submission_is_allowed(student, task):
    make_submission(student, task, Submission.Status.ACTIVE)
    with pytest.raises(IntegrityError), transaction.atomic():
        make_submission(student, task, Submission.Status.ACTIVE)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("score", "expected"), [(59, False), (60, True), (100, True)]
)
def test_generated_passing_flag_tracks_score(student, task, score, expected):
    submission = make_submission(
        student, task, Submission.Status.COMPLETED, score=score
    )
    submission.refresh_from_db()
    assert submission.is_passing is expected


@pytest.mark.django_db
def test_task_slug_and_legacy_numeric_detail_url(task):
    assert task.slug == f"prakticheskaia-rabota-{task.pk}"
    assert task.get_absolute_url() == reverse(
        "tasks:detail", kwargs={"slug": task.slug}
    )
    client = Client()
    assert client.get(task.get_absolute_url()).status_code == 200
    legacy_url = reverse("tasks:detail", args=[task.pk])
    assert client.get(legacy_url).status_code == 200


@pytest.mark.django_db
def test_submission_list_filters_and_preserves_get_parameters(student, task):
    make_submission(student, task, Submission.Status.ACTIVE)
    make_submission(
        student, task, Submission.Status.CANCELLED, day=date(2026, 11, 2)
    )
    client = Client()
    response = client.get(
        reverse("submissions:list"),
        {
            "status": Submission.Status.ACTIVE,
            "date": "2026-11-01",
            "task": task.pk,
            "student": student.pk,
        },
    )

    assert response.status_code == 200
    assert response.context["page_obj"].paginator.count == 1
    assert response.context["selected_status"] == Submission.Status.ACTIVE
    assert response.context["query_params"] == (
        f"status=active&date=2026-11-01&task={task.pk}&student={student.pk}"
    )


@pytest.mark.django_db
def test_admin_registers_models_and_related_inlines():
    assert Student in admin.site._registry
    assert Task in admin.site._registry
    assert Submission in admin.site._registry
    assert StudentAdmin.inlines
    assert TaskAdmin.inlines
    assert "status" in SubmissionAdmin.list_display
    assert "status" in SubmissionAdmin.list_filter


@pytest.mark.django_db
def test_admin_pages_render_related_records(student, task):
    make_submission(student, task, Submission.Status.ACTIVE)
    admin_user = get_user_model().objects.create_superuser(
        username="pr10-admin",
        email="pr10-admin@example.test",
        password="test-password",
    )
    client = Client()
    client.force_login(admin_user)

    student_page = client.get(
        reverse("admin:students_student_change", args=[student.pk])
    )
    submission_page = client.get(
        reverse("admin:submissions_submission_changelist")
    )

    assert student_page.status_code == 200
    assert submission_page.status_code == 200
    assert "Сдачи" in student_page.content.decode()
    assert "Статус" in submission_page.content.decode()


@pytest.mark.django_db
def test_homepage_exposes_status_statistics_and_shared_context(student, task):
    before = Submission.objects.aggregate(
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
    )
    make_submission(student, task, Submission.Status.ACTIVE)
    make_submission(
        student,
        task,
        Submission.Status.CANCELLED,
        day=date(2026, 11, 2),
    )
    make_submission(
        student,
        task,
        Submission.Status.COMPLETED,
        day=date(2026, 11, 3),
        score=80,
    )

    response = Client().get(reverse("homepage:index"))

    assert response.status_code == 200
    for key in before:
        assert response.context["statistics"][key] == before[key] + 1
    assert response.context["site_task_count"] == Task.objects.count()
