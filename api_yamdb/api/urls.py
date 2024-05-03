"""Api app URL configuration."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)
from api.views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    ReviewViewSet,
    CommentViewSet,
)

from .constants import API_VERSION

app_name = 'api'

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='title')
router.register('genres', GenreViewSet, basename='genre')
router.register('categories', CategoryViewSet, basename='category')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet, basename='comment')

urlpatterns = [
    path(f'{API_VERSION}/', include('users.urls')),
    path(f'{API_VERSION}/', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # Временно
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),  # Временно
]
