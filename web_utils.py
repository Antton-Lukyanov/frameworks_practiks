"""Shared helpers for the Django list pages."""

from django.core.paginator import Paginator


def paginate_queryset(request, queryset, per_page=8):
    page_obj = Paginator(queryset, per_page).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return page_obj, params.urlencode()
