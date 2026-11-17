"""РљРѕСЂРЅРµРІР°СЏ РјР°СЂС€СЂСѓС‚РёР·Р°С†РёСЏ Django-РїСЂРѕРµРєС‚Р°."""

from django.contrib import admin
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("students/", include("students.urls")),
    path("tasks/", include("tasks.urls")),
    path("submissions/", include("submissions.urls")),
]

handler404 = "homepage.views.page_not_found"

admin.site.site_header = "Сервис сдачи заданий — администрирование"
admin.site.site_title = "Администрирование сервиса"
admin.site.index_title = "Управление данными проекта"

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
