from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Case, Q, Value, When

from students.models import Student
from tasks.models import Task


class SubmissionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=self.model.Status.CANCELLED)

    def completed(self):
        return self.filter(status=self.model.Status.COMPLETED)

    def for_date(self, selected_date):
        return self.filter(submission_date=selected_date)

    def not_cancelled(self):
        return self.exclude(status=self.model.Status.CANCELLED)


class SubmissionManager(models.Manager.from_queryset(SubmissionQuerySet)):
    pass


class SubmissionStatus(models.TextChoices):
    ACTIVE = "active", "Активна"
    CANCELLED = "cancelled", "Отменена"
    COMPLETED = "completed", "Проверена"


class Submission(models.Model):
    Status = SubmissionStatus

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="студент",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="задание",
    )
    file_name = models.CharField("Имя файла", max_length=255)
    file_size_mb = models.DecimalField(
        "Размер файла, МБ",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    score = models.PositiveSmallIntegerField("Баллы", default=0)
    submission_date = models.DateField("Дата сдачи")
    status = models.CharField(
        "Статус",
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    is_passing = models.GeneratedField(
        expression=Case(
            When(score__gte=60, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Зачтена",
    )
    objects = SubmissionManager()

    class Meta:
        ordering = ["-submission_date", "-id"]
        verbose_name = "сдача"
        verbose_name_plural = "сдачи"
        constraints = [
            models.UniqueConstraint(
                fields=("student", "task"),
                condition=Q(status=SubmissionStatus.ACTIVE),
                name="unique_active_submission_per_student_task",
            ),
        ]

    def __str__(self):
        return f"{self.student} — {self.task} ({self.submission_date})"

    def get_result(self):
        if self.score >= 80:
            return "Отлично"
        if self.score >= 60:
            return "Хорошо"
        return "Требуется доработка"
