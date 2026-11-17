# Сервис сдачи заданий

Учебное приложение для учёта студентов, заданий и их сдачи. Консольная версия
из ПР3 дополнена веб-интерфейсом на Django. В ПР6 HTML-представления переведены
с Python-строк на Django Template Language.

## Предметная область и данные

- `Student` — студент, имя и учебная группа;
- `Task` — задание, максимальный балл и дедлайн;
- `Submission` — сдача задания студентом, имя файла, размер, дата, балл и статус
  `ACTIVE`, `CANCELLED` или `COMPLETED`. Статус перенесён из прежнего булева
  признака миграцией данных; связанные записи не удаляются. QuerySet предоставляет
  выборки по статусу и дате. Поле `is_passing` вычисляется SQLite по оценке
  (порог зачёта — 60 баллов).

Основные данные веб-приложения хранятся в SQLite и описаны Django-моделями в
`students/models.py`, `tasks/models.py` и `submissions/models.py`. Связь сдачи
со студентом и заданием реализована через `ForeignKey`. Миграция переносит
записи из `db/project.sqlite3`, если эта база ПР7 доступна, или из версионируемых
JSON-файлов как резервного источника. Консольная программа `main.py` и модели из
верхнеуровневого пакета `models/` сохранены для прежних практических работ.
SQL-схема и набор ручных SQL-запросов ПР7 остаются в `sql/`.

## Технологии

- Python 3.10+;
- Django 5.2 и Django Template Language;
- HTML5, CSS3, JavaScript и Bootstrap 5.3;
- Django ORM и SQLite для веб-интерфейса;
- JSON для консольной версии и переноса исходных данных;
- pytest и flake8 для проверки консольного проекта.

## Страницы

| URL | Назначение | View |
| --- | --- | --- |
| `/` | Главная страница и навигация | `homepage.views.index()` |
| `/students/` | Список студентов | `students.views.student_list()` |
| `/students/<int:student_id>/` | Карточка студента | `students.views.student_detail()` |
| `/tasks/` | Список заданий | `tasks.views.task_list()` |
| `/tasks/<int:task_id>/` | Карточка задания | `tasks.views.task_detail()` |
| `/submissions/` | Список сдач | `submissions.views.submission_list()` |
| `/submissions/<int:submission_id>/` | Карточка сдачи | `submissions.views.submission_detail()` |
| `/admin/` | Управление данными | Django Admin |

Несуществующие карточки возвращают HTTP 404 и показывают сообщение из шаблона.
Ссылки в HTML строятся через именованные маршруты с пространствами имён,
например `{% url 'tasks:detail' task.id %}`.

## Шаблоны и статические файлы

- `templates/base.html` — общий каркас, Bootstrap, собственный CSS, навигация и
  подвал;
- `templates/includes/navigation.html` — общее меню;
- `homepage/templates/homepage/` — главная страница;
- `students/templates/students/`, `tasks/templates/tasks/` и
  `submissions/templates/submissions/` — списки, карточки и подключаемые
  фрагменты сущностей;
- `homepage/static/homepage/css/style.css` — собственные стили;
- `homepage/static/homepage/js/main.js` — текущий год в подвале;
- `homepage/static/homepage/img/logo.svg` — логотип навигации.

Страницы наследуют `base.html`; повторяющиеся карточки и статус сдачи вынесены
в `include`. Циклы, ветвления и фильтры `length` и `default` выполняются в
шаблонах. Представления только загружают данные, готовят контекст и вызывают
`render()`; функция `page()` из ПР5 удалена.

## Установка и запуск

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver --insecure
```

Для управления записями через `/admin/` создайте администратора командой
`python manage.py createsuperuser`.

Откройте <http://127.0.0.1:8000/>. Флаг `--insecure` включает раздачу
статических файлов встроенным сервером при `DEBUG = False`; это подходит только
для локальной разработки. Консольная версия запускается командой
`python main.py`.

## Состояние проекта

Списки студентов, заданий и сдач поддерживают поиск, фильтрацию, сортировку и
пагинацию. Список сдач фильтруется по статусу, дате, заданию и студенту; выбранные
параметры сохраняются при переходе по страницам. Карточки показывают связанные
записи; выборки используют `select_related()` и `prefetch_related()`. Подробная
страница задания использует транслитерированный slug. Главная страница показывает
статистику по статусам и оценкам. Контекстный процессор передаёт общую навигацию
и количество заданий.

## Django Admin и отладка ORM

Административная панель русифицирована и позволяет управлять студентами,
заданиями и сдачами. В списках настроены столбцы, фильтры, поиск, сортировка и
размер страницы; в карточках студентов и заданий встроены связанные сдачи. Для
локального анализа SQL включён Django Debug Toolbar по адресу `/__debug__/`.

Проверки моделей и миграций:

```powershell
python manage.py check
python manage.py showmigrations
python manage.py makemigrations --check
pytest -v
```
