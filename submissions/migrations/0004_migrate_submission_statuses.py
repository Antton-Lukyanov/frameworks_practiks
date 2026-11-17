from django.db import migrations, models
from django.db.models import Q


def migrate_statuses(apps, schema_editor):
    Submission = apps.get_model("submissions", "Submission")
    database = schema_editor.connection.alias

    Submission.objects.using(database).filter(is_cancelled=True).update(
        status="cancelled"
    )
    Submission.objects.using(database).filter(is_cancelled=False).update(
        status="active"
    )


def reverse_statuses(apps, schema_editor):
    Submission = apps.get_model("submissions", "Submission")
    database = schema_editor.connection.alias

    # The former boolean cannot represent COMPLETED. Map it to the legacy
    # inactive state so completed history remains stored without violating
    # the old one-non-cancelled-submission constraint on rollback.
    Submission.objects.using(database).filter(
        status__in=("cancelled", "completed")
    ).update(is_cancelled=True)
    Submission.objects.using(database).filter(status="active").update(
        is_cancelled=False
    )


class Migration(migrations.Migration):
    dependencies = [
        ("submissions", "0003_add_status_and_passing_flag"),
        ("tasks", "0002_add_populated_slug"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="submission",
            name="unique_active_submission_per_student_task",
        ),
        migrations.RunPython(migrate_statuses, reverse_statuses),
        migrations.RemoveField(
            model_name="submission",
            name="is_cancelled",
        ),
        migrations.AddConstraint(
            model_name="submission",
            constraint=models.UniqueConstraint(
                condition=Q(status="active"),
                fields=("student", "task"),
                name="unique_active_submission_per_student_task",
            ),
        ),
    ]
