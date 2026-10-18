"""Главная страница и общий HTML-каркас сайта."""

from django.http import HttpResponse
from django.utils.html import escape


def page(title: str, content: str) -> str:
    """Собрать общий HTML-каркас с навигацией и Bootstrap."""
    bootstrap_css = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )
    return f"""<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link href="{bootstrap_css}" rel="stylesheet">
    <style>
        body {{ background-color: #f8f9fa; }}
        .navbar-nav {{ flex-direction: row; gap: 0.5rem; }}
        .list-group-item a {{ text-decoration: none; }}
        .list-group-item a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">Сервис заданий</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/students/">Студенты</a>
                <a class="nav-link" href="/tasks/">Задания</a>
                <a class="nav-link" href="/submissions/">Сдачи</a>
            </div>
        </div>
    </nav>
    <main class="container py-5">{content}</main>
</body>
</html>"""


def index(request):
    """Показать главную страницу веб-интерфейса."""
    content = """
    <section class="p-5 mb-4 bg-light rounded-3">
        <h1 class="display-5 fw-bold">Сервис сдачи заданий</h1>
        <p class="col-md-8 fs-5">Веб-интерфейс для просмотра студентов,
        учебных заданий и результатов их сдачи.</p>
        <a href="/students/" class="btn btn-primary btn-lg me-2">Студенты</a>
        <a href="/tasks/" class="btn btn-outline-primary btn-lg me-2">
            Задания</a>
        <a href="/submissions/" class="btn btn-outline-primary btn-lg">
            Сдачи</a>
    </section>
    <p class="text-muted">Данные загружаются из JSON-файлов проекта.</p>
    """
    return HttpResponse(page("Сервис сдачи заданий", content))


def page_not_found(request, exception):
    """Показать оформленную страницу для неизвестного адреса."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную страницу.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(page("Страница не найдена", content), status=404)
