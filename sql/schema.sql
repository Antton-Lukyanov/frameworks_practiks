PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    "group" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    max_score INTEGER NOT NULL CHECK (max_score >= 0),
    deadline TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_size_mb REAL NOT NULL CHECK (file_size_mb >= 0),
    score INTEGER NOT NULL DEFAULT 0 CHECK (score >= 0),
    submission_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0 CHECK (is_cancelled IN (0, 1)),
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_submissions_student_id
    ON submissions (student_id);
CREATE INDEX IF NOT EXISTS idx_submissions_task_id
    ON submissions (task_id);
CREATE INDEX IF NOT EXISTS idx_tasks_deadline
    ON tasks (deadline);
