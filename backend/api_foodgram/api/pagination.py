from rest_framework.pagination import PageNumberPagination


class RecipeUserPagination(PageNumberPagination):
    page_size_query_param = 'limit'
