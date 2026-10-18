# Сервис сдачи заданий

Учебное приложение для учёта студентов, заданий и их сдачи. Консольная версия
из ПР3 дополнена веб-интерфейсом на Django. В ПР6 HTML-представления переведены
с Python-строк на Django Template Language.

## Предметная область и данные

- `Student` — студент, имя и учебная группа;
- `Task` — задание, максимальный балл и дедлайн;
- `Submission` — сдача задания студентом, имя файла, размер, дата, балл и статус.

Данные загружаются из `data/students.json`, `data/tasks.json` и
`data/submissions.json`. Веб-представления используют классы и функции из
`models/` и загрузчики из `storage.py`. Django ORM, миграции и формы пока не
используются. Консольная программа `main.py` и её тесты сохранены.

## Технологии

- Python 3.10+;
- Django 5.2 и Django Template Language;
- HTML5, CSS3, JavaScript и Bootstrap 5.3;
- JSON как хранилище данных;
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
python manage.py runserver --insecure
```

Откройте <http://127.0.0.1:8000/>. Флаг `--insecure` включает раздачу
статических файлов встроенным сервером при `DEBUG = False`; это подходит только
для локальной разработки. Консольная версия запускается командой
`python main.py`.

## Состояние проекта

Веб-интерфейс поддерживает просмотр списков и карточек. Добавление и изменение
записей через формы, аутентификация, Django ORM и работа с базой данных относятся
к следующим этапам.
