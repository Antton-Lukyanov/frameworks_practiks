"""Parameterized SQL queries used by the web pages."""

from __future__ import annotations

from db.database import database_connection


def fetch_students():
    with database_connection() as connection:
        return connection.execute(
            'SELECT id, name, "group" FROM students ORDER BY name, id'
        ).fetchall()


def fetch_student(student_id: int):
    with database_connection() as connection:
        return connection.execute(
            'SELECT id, name, "group" FROM students WHERE id = ?',
            (student_id,),
        ).fetchone()


def fetch_tasks():
    with database_connection() as connection:
        return connection.execute(
            "SELECT id, title, max_score, deadline FROM tasks ORDER BY deadline, id"
        ).fetchall()


def fetch_task(task_id: int):
    with database_connection() as connection:
        return connection.execute(
            "SELECT id, title, max_score, deadline FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()


def fetch_submissions():
    with database_connection() as connection:
        return connection.execute(
            "SELECT s.id, s.student_id, s.task_id, s.file_name, s.file_size_mb, "
            "s.score, s.submission_date, s.is_cancelled, "
            'st.name AS student_name, st."group" AS student_group, '
            "t.title AS task_title, t.max_score, t.deadline "
            "FROM submissions AS s "
            "JOIN students AS st ON st.id = s.student_id "
            "JOIN tasks AS t ON t.id = s.task_id "
            "ORDER BY s.submission_date DESC, s.id DESC"
        ).fetchall()


def fetch_submission(submission_id: int):
    with database_connection() as connection:
        return connection.execute(
            "SELECT s.id, s.student_id, s.task_id, s.file_name, s.file_size_mb, "
            "s.score, s.submission_date, s.is_cancelled, "
            'st.name AS student_name, st."group" AS student_group, '
            "t.title AS task_title, t.max_score, t.deadline "
            "FROM submissions AS s "
            "JOIN students AS st ON st.id = s.student_id "
            "JOIN tasks AS t ON t.id = s.task_id "
            "WHERE s.id = ?",
            (submission_id,),
        ).fetchone()
