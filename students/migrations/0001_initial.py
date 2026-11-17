from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Student",
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
                    "name",
                    models.CharField(
                        max_length=120, verbose_name="Имя"
                    ),
                ),
                (
                    "group",
                    models.CharField(max_length=40, verbose_name="Группа"),
                ),
            ],
            options={
                "verbose_name": "студент",
                "verbose_name_plural": "студенты",
                "ordering": ["name", "id"],
            },
        ),
    ]
