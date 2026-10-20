"""РџСЂРµРґСЃС‚Р°РІР»РµРЅРёСЏ СЃРїРёСЃРєР° СЃС‚СѓРґРµРЅС‚РѕРІ Рё РєР°СЂС‚РѕС‡РєРё СЃС‚СѓРґРµРЅС‚Р°."""

from django.conf import settings
from django.shortcuts import render

from models.students import get_student_by_id
from storage import load_students


def student_list(request):
    """РџРѕРєР°Р·Р°С‚СЊ СЃС‚СѓРґРµРЅС‚РѕРІ, Р·Р°РіСЂСѓР¶РµРЅРЅС‹С… РёР· JSON."""
    filename = settings.BASE_DIR / "data/students.json"
    students = load_students(str(filename))
    return render(request, "students/student_list.html", {"students": students})


def student_detail(request, student_id):
    """РџРѕРєР°Р·Р°С‚СЊ РєР°СЂС‚РѕС‡РєСѓ СЃС‚СѓРґРµРЅС‚Р° РёР»Рё С€Р°Р±Р»РѕРЅ РѕС€РёР±РєРё СЃ HTTP 404."""
    filename = settings.BASE_DIR / "data/students.json"
    students = load_students(str(filename))
    student = get_student_by_id(students, student_id)
    return render(
        request,
        "students/student_detail.html",
        {"student": student},
        status=404 if student is None else 200,
    )

