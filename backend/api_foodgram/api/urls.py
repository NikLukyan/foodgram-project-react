from django.urls import include, path, re_path
from rest_framework import routers

from .views import (
    UserViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
# router.register(r'titles', TitlesViewSet, basename='titles')
# router.register(r'genres', GenresViewSet, basename='genres')
# router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='review',
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment',
# )

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
