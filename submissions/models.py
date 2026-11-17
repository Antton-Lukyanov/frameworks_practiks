from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from students.models import Student
from tasks.models import Task


class Submission(models.Model):
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
    is_cancelled = models.BooleanField("Отменена", default=False)

    class Meta:
        ordering = ["-submission_date", "-id"]
        verbose_name = "сдача"
        verbose_name_plural = "сдачи"
        constraints = [
            models.UniqueConstraint(
                fields=("student", "task"),
                condition=Q(is_cancelled=False),
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
