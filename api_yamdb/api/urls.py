"""Api app URL configuration."""
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)

from .constants import API_VERSION

urlpatterns = [
    path(f'{API_VERSION}/', include('users.urls')),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # Временно
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),  # Временно
]
