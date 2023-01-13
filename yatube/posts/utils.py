from django.core.paginator import Paginator


NUMBERS_PAGES = 10


def get_page(queryset: str, request: any) -> dict:
    """Функция для разбиения записей из базы данных
    постранично.
    """
    paginator = Paginator(queryset, NUMBERS_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
    }
