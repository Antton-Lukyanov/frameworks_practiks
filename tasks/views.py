"""РџСЂРµРґСЃС‚Р°РІР»РµРЅРёСЏ СЃРїРёСЃРєР° Р·Р°РґР°РЅРёР№ Рё РєР°СЂС‚РѕС‡РєРё Р·Р°РґР°РЅРёСЏ."""

from django.conf import settings
from django.shortcuts import render

from models.tasks import get_task_by_id
from storage import load_tasks


def task_list(request):
    """РџРѕРєР°Р·Р°С‚СЊ СѓС‡РµР±РЅС‹Рµ Р·Р°РґР°РЅРёСЏ, Р·Р°РіСЂСѓР¶РµРЅРЅС‹Рµ РёР· JSON."""
    tasks = load_tasks(str(settings.BASE_DIR / "data/tasks.json"))
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_detail(request, task_id):
    """РџРѕРєР°Р·Р°С‚СЊ РєР°СЂС‚РѕС‡РєСѓ Р·Р°РґР°РЅРёСЏ РёР»Рё С€Р°Р±Р»РѕРЅ РѕС€РёР±РєРё СЃ HTTP 404."""
    tasks = load_tasks(str(settings.BASE_DIR / "data/tasks.json"))
    task = get_task_by_id(tasks, task_id)
    return render(
        request,
        "tasks/task_detail.html",
        {"task": task},
        status=404 if task is None else 200,
    )

