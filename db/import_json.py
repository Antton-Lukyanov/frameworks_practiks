"""Import the existing JSON records into SQLite without duplicating rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3

from db.database import DATABASE_PATH, PROJECT_DIR, get_connection


def _read_records(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as source:
        records = json.load(source)
    if not isinstance(records, list):
        raise ValueError(f"Expected a JSON list in {path}")
    return records


def import_json_data(
    connection: sqlite3.Connection,
    data_dir: str | Path = PROJECT_DIR / "data",
) -> tuple[int, int, int]:
    """Upsert students, tasks and submissions in one transaction."""
    data_dir = Path(data_dir)
    students = _read_records(data_dir / "students.json")
    tasks = _read_records(data_dir / "tasks.json")
    submissions = _read_records(data_dir / "submissions.json")

    with connection:
        connection.executemany(
            'INSERT INTO students (id, name, "group") VALUES (?, ?, ?) '
            'ON CONFLICT(id) DO UPDATE SET name=excluded.name, "group"=excluded."group"',
            [(item["id"], item["name"], item["group"]) for item in students],
        )
        connection.executemany(
            "INSERT INTO tasks (id, title, max_score, deadline) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET title=excluded.title, "
            "max_score=excluded.max_score, deadline=excluded.deadline",
            [
                (item["id"], item["title"], item["max_score"], item["deadline"])
                for item in tasks
            ],
        )
        connection.executemany(
            "INSERT INTO submissions "
            "(id, student_id, task_id, file_name, file_size_mb, score, "
            "submission_date, is_cancelled) VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET student_id=excluded.student_id, "
            "task_id=excluded.task_id, file_name=excluded.file_name, "
            "file_size_mb=excluded.file_size_mb, score=excluded.score, "
            "submission_date=excluded.submission_date, "
            "is_cancelled=excluded.is_cancelled",
            [
                (
                    item["id"],
                    item["student_id"],
                    item["task_id"],
                    item["file_name"],
                    item["file_size_mb"],
                    item["score"],
                    item["submission_date"],
                    int(item.get("is_cancelled", False)),
                )
                for item in submissions
            ],
        )
    return len(students), len(tasks), len(submissions)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=PROJECT_DIR / "data",
        help="directory containing students.json, tasks.json and submissions.json",
    )
    parser.add_argument("--database", type=Path, default=DATABASE_PATH)
    args = parser.parse_args()

    connection = get_connection(args.database)
    try:
        counts = import_json_data(connection, args.data_dir)
    finally:
        connection.close()
    print(
        "Imported: "
        f"{counts[0]} students, {counts[1]} tasks, {counts[2]} submissions."
    )


if __name__ == "__main__":
    main()
