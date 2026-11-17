def site_metadata(request):
    if request.path.startswith("/admin/"):
        return {}

    from tasks.models import Task

    return {
        "site_name": "Сервис сдачи заданий",
        "site_task_count": Task.objects.count(),
    }
