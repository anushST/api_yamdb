"""Users app URL configuration."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GetTokenAPIView, SignupAPIView, UserApiView,
                    UserViewSetForAdmin)

router = DefaultRouter()
router.register('users', UserViewSetForAdmin, basename='user-for-admin')

urlpatterns = [
    path('users/me/', UserApiView.as_view(), name='user'),
    path('auth/signup/', SignupAPIView.as_view(), name='signup'),
    path('auth/token/', GetTokenAPIView.as_view(), name='token'),
    path('', include(router.urls)),
]
