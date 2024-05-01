"""Users app URL configuration."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserApiView, UserViewSetForAdmin

router = DefaultRouter()
router.register('users', UserViewSetForAdmin, basename='user-for-admin')

urlpatterns = [
    path('users/me/', UserApiView.as_view(), name='user'),
    path('', include(router.urls)),
]
