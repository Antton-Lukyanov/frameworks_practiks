from django.db import migrations, models
from django.utils.text import slugify
from unidecode import unidecode


def populate_task_slugs(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    database = schema_editor.connection.alias

    for task in Task.objects.using(database).all().order_by("pk"):
        base_slug = slugify(unidecode(task.title)) or "task"
        Task.objects.using(database).filter(pk=task.pk).update(
            slug=f"{base_slug[:160]}-{task.pk}"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
        ("submissions", "0002_import_pr7_json"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="slug",
            field=models.SlugField(
                blank=True,
                editable=False,
                max_length=180,
                verbose_name="URL-идентификатор",
            ),
        ),
        migrations.RunPython(
            populate_task_slugs,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="task",
            name="slug",
            field=models.SlugField(
                editable=False,
                max_length=180,
                unique=True,
                verbose_name="URL-идентификатор",
            ),
        ),
    ]
