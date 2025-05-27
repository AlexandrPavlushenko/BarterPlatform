from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Стандартная пагинация для наборов результатов API.

    Настройки пагинации:
    - page_size: Количество элементов на странице по умолчанию (10)
    - page_size_query_param: Параметр запроса для изменения размера страницы
    - max_page_size: Максимально допустимый размер страницы (10)
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10
