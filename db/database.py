"""SQLite connection helpers used by the Django views."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_DIR / "db" / "project.sqlite3"
SCHEMA_PATH = PROJECT_DIR / "sql" / "schema.sql"


def get_connection(database_path: str | Path | None = None) -> sqlite3.Connection:
    """Open the project database and ensure its schema and FK checks are active."""
    path = Path(database_path) if database_path else DATABASE_PATH
    is_new_database = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection.executescript(schema)
    if is_new_database and path.resolve() == DATABASE_PATH.resolve():
        from db.import_json import import_json_data

        import_json_data(connection)
    return connection


@contextmanager
def database_connection() -> Iterator[sqlite3.Connection]:
    """Yield a database connection and always close it after the operation."""
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()
