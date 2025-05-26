from rest_framework.pagination import PageNumberPagination


class AdListPagination(PageNumberPagination):
    """Пагинатор объявлений"""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 5


    class ExchangeProposalPaginator(PageNumberPagination):
        """Пагинатор объявлений"""

        page_size = 5
        page_size_query_param = "page_size"
        max_page_size = 5