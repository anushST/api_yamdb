from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    ReviewViewSet,
    CommentViewSet,
)
from .constants import API_VERSION


app_name = 'api'

router = SimpleRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet, basename='comment')

urlpatterns = [
    path(f'{API_VERSION}/', include('djoser.urls')),
    path(f'{API_VERSION}/', include('djoser.urls.jwt')),
    path(f'{API_VERSION}/', include(router.urls)),
]
