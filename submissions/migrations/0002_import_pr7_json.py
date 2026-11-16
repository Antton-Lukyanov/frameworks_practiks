import json
from pathlib import Path
import sqlite3

from django.db import migrations


def read_pr7_records(project_dir, table, columns, json_name):
    legacy_database = project_dir / "db" / "project.sqlite3"
    if legacy_database.exists():
        uri = legacy_database.as_uri() + "?mode=ro"
        with sqlite3.connect(uri, uri=True) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
            if table in tables:
                records = connection.execute(
                    f"SELECT {', '.join(columns)} FROM {table}"
                ).fetchall()
                if records:
                    return [dict(zip(columns, row)) for row in records]

    with (project_dir / "data" / json_name).open(encoding="utf-8") as source:
        return json.load(source)


def import_pr7_data(apps, schema_editor):
    project_dir = Path(__file__).resolve().parents[2]
    Student = apps.get_model("students", "Student")
    Task = apps.get_model("tasks", "Task")
    Submission = apps.get_model("submissions", "Submission")

    students = read_pr7_records(
        project_dir, "students", ("id", "name", "group"), "students.json"
    )
    tasks = read_pr7_records(
        project_dir,
        "tasks",
        ("id", "title", "max_score", "deadline"),
        "tasks.json",
    )
    submissions = read_pr7_records(
        project_dir,
        "submissions",
        (
            "id",
            "student_id",
            "task_id",
            "file_name",
            "file_size_mb",
            "score",
            "submission_date",
            "is_cancelled",
        ),
        "submissions.json",
    )

    database = schema_editor.connection.alias
    Student.objects.using(database).bulk_create(
        [
            Student(id=item["id"], name=item["name"], group=item["group"])
            for item in students
        ]
    )
    Task.objects.using(database).bulk_create(
        [
            Task(
                id=item["id"],
                title=item["title"],
                max_score=item["max_score"],
                deadline=item["deadline"],
            )
            for item in tasks
        ]
    )
    student_ids = {item["id"] for item in students}
    task_ids = {item["id"] for item in tasks}
    Submission.objects.using(database).bulk_create(
        [
            Submission(
                id=item["id"],
                student_id=item["student_id"],
                task_id=item["task_id"],
                file_name=item["file_name"],
                file_size_mb=item["file_size_mb"],
                score=item["score"],
                submission_date=item["submission_date"],
                is_cancelled=item.get("is_cancelled", False),
            )
            for item in submissions
            if (
                item["student_id"] in student_ids
                and item["task_id"] in task_ids
            )
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0001_initial"),
        ("tasks", "0001_initial"),
        ("submissions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(import_pr7_data, migrations.RunPython.noop)
    ]
