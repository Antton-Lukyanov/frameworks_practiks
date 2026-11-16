import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("students", "0001_initial"),
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file_name",
                    models.CharField(
                        max_length=255, verbose_name="Имя файла"
                    ),
                ),
                (
                    "file_size_mb",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=8,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                        verbose_name="Размер файла, МБ",
                    ),
                ),
                (
                    "score",
                    models.PositiveSmallIntegerField(
                        default=0,
                        verbose_name="Баллы",
                    ),
                ),
                (
                    "submission_date",
                    models.DateField(verbose_name="Дата сдачи"),
                ),
                (
                    "is_cancelled",
                    models.BooleanField(
                        default=False, verbose_name="Отменена"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="students.student",
                        verbose_name="студент",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="tasks.task",
                        verbose_name="задание",
                    ),
                ),
            ],
            options={
                "verbose_name": "сдача",
                "verbose_name_plural": "сдачи",
                "ordering": ["-submission_date", "-id"],
            },
        ),
        migrations.AddConstraint(
            model_name="submission",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_cancelled", False)),
                fields=("student", "task"),
                name="unique_active_submission_per_student_task",
            ),
        ),
    ]
