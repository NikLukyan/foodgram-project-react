from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    """Пагинация пользователей по параметрам limit и page."""
    page_size_query_param = 'limit'


class RecipePagination(PageNumberPagination):
    """Пагинация рецептов по параметрам limit и page."""
    page_size_query_param = 'limit'
