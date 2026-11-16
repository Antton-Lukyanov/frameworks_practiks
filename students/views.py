"""Student list and detail pages backed by SQLite."""

from django.shortcuts import render

from db.queries import fetch_student, fetch_students


def student_list(request):
    return render(
        request,
        "students/student_list.html",
        {"students": fetch_students()},
    )


def student_detail(request, student_id):
    student = fetch_student(student_id)
    return render(
        request,
        "students/student_detail.html",
        {"student": student},
        status=404 if student is None else 200,
    )
