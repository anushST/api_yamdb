"""Users app URL configuration."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenAPIView, SignupAPIView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user-for-admin')

user_view_set = UserViewSet.as_view({
    'get': 'current_user',
    'patch': 'current_user',
})

urlpatterns = [
    path('users/me/', user_view_set, name='user'),
    path('auth/signup/', SignupAPIView.as_view(), name='signup'),
    path('auth/token/', GetTokenAPIView.as_view(), name='token'),
    path('', include(router.urls)),
]
