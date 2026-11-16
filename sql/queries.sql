-- 1. Read all students.
SELECT id, name, "group" FROM students ORDER BY name;

-- 2. Filter students by study group (parameter: :group_name).
SELECT id, name FROM students WHERE "group" = :group_name ORDER BY name;

-- 3. Tasks due by a date (parameter: :deadline).
SELECT id, title, deadline FROM tasks WHERE deadline <= :deadline ORDER BY deadline;

-- 4. Submission details joined to the student and task tables.
SELECT s.id, st.name, t.title, s.file_name, s.score, s.submission_date
FROM submissions AS s
JOIN students AS st ON st.id = s.student_id
JOIN tasks AS t ON t.id = s.task_id
ORDER BY s.submission_date DESC;

-- 5. Number of active submissions and average score per student.
SELECT st.id, st.name, COUNT(s.id) AS submission_count,
       AVG(NULLIF(s.score, 0)) AS average_score
FROM students AS st
LEFT JOIN submissions AS s ON s.student_id = st.id AND s.is_cancelled = 0
GROUP BY st.id, st.name
ORDER BY st.name;

-- 6. Submission count per task, including tasks with no submissions.
SELECT t.id, t.title, COUNT(s.id) AS submission_count
FROM tasks AS t
LEFT JOIN submissions AS s ON s.task_id = t.id AND s.is_cancelled = 0
GROUP BY t.id, t.title
ORDER BY submission_count DESC;

-- 7. Student counts and average score by study group.
SELECT st."group", COUNT(DISTINCT st.id) AS student_count,
       AVG(NULLIF(s.score, 0)) AS average_score
FROM students AS st
LEFT JOIN submissions AS s ON s.student_id = st.id AND s.is_cancelled = 0
GROUP BY st."group";

-- 8. Groups whose average score is at least :minimum_score (HAVING).
SELECT st."group", AVG(s.score) AS average_score
FROM students AS st
JOIN submissions AS s ON s.student_id = st.id AND s.is_cancelled = 0
WHERE s.score > 0
GROUP BY st."group"
HAVING AVG(s.score) >= :minimum_score;

-- 9. Students with no active submissions (NOT EXISTS subquery).
SELECT st.id, st.name
FROM students AS st
WHERE NOT EXISTS (
    SELECT 1 FROM submissions AS s
    WHERE s.student_id = st.id AND s.is_cancelled = 0
);

-- 10. Highest score for each task (correlated subquery).
SELECT t.id, t.title, (
    SELECT MAX(s.score) FROM submissions AS s
    WHERE s.task_id = t.id AND s.is_cancelled = 0
) AS highest_score
FROM tasks AS t;

-- 11. Active submissions with results grouped by feedback category.
SELECT CASE WHEN score >= 80 THEN 'excellent'
            WHEN score >= 60 THEN 'good' ELSE 'needs_revision' END AS result,
       COUNT(*) AS submission_count
FROM submissions
WHERE is_cancelled = 0
GROUP BY result;

-- 12. Tasks that do not have any active submissions.
SELECT t.id, t.title
FROM tasks AS t
LEFT JOIN submissions AS s ON s.task_id = t.id AND s.is_cancelled = 0
WHERE s.id IS NULL;
