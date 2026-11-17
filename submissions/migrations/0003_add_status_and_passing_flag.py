from django.db import migrations, models
from django.db.models import Case, Value, When


class Migration(migrations.Migration):
    dependencies = [
        ("submissions", "0002_import_pr7_json"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="status",
            field=models.CharField(
                choices=[
                    ("active", "Активна"),
                    ("cancelled", "Отменена"),
                    ("completed", "Проверена"),
                ],
                default="active",
                max_length=12,
                verbose_name="Статус",
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="is_passing",
            field=models.GeneratedField(
                db_persist=True,
                expression=Case(
                    When(score__gte=60, then=Value(True)),
                    default=Value(False),
                    output_field=models.BooleanField(),
                ),
                output_field=models.BooleanField(),
                verbose_name="Зачтена",
            ),
        ),
    ]
