from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
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
                    "title",
                    models.CharField(max_length=200, verbose_name="Название"),
                ),
                (
                    "max_score",
                    models.PositiveSmallIntegerField(
                        default=100,
                        verbose_name="Максимальный балл",
                    ),
                ),
                ("deadline", models.DateField(verbose_name="Срок сдачи")),
            ],
            options={
                "verbose_name": "задание",
                "verbose_name_plural": "задания",
                "ordering": ["deadline", "id"],
            },
        ),
    ]
