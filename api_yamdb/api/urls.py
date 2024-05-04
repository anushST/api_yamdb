"""Api app URL configuration."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)
from api.views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
)

from .constants import API_VERSION

app_name = 'api'

router = DefaultRouter()
router.register('titles', TitleViewSet,)
router.register('genres', GenreViewSet,)
router.register('categories', CategoryViewSet,)


urlpatterns = [
    path(f'{API_VERSION}/', include('users.urls')),
    path(f'{API_VERSION}/', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # Временно
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),  # Временно
]
