# """Api app URL configuration."""
# from django.urls import include, path
# from rest_framework.routers import SimpleRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView, TokenRefreshView,)
# from api.views import (
#     TitleViewSet,
#     GenreViewSet,
#     CategoryViewSet,
#     ReviewViewSet,
#     CommentViewSet,
# )

# from .constants import API_VERSION

# app_name = 'api'

# router = SimpleRouter()
# router.register('titles', TitleViewSet)
# router.register('genres', GenreViewSet)
# router.register('categories', CategoryViewSet)
# router.register(
#     r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet, basename='review')
# router.register(
#     r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
#     CommentViewSet, basename='comment')

# urlpatterns = [
#     path(f'{API_VERSION}/', include('users.urls')),
#     path(f'{API_VERSION}/', include(router.urls)),
#     path('token/', TokenObtainPairView.as_view(),
#          name='token_obtain_pair'),  # Временно
#     path('token/refresh/', TokenRefreshView.as_view(),
#          name='token_refresh'),  # Временно
# ]


"""Api app URL configuration."""
from django.urls import include, path
from rest_framework.routers import SimpleRouter
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

router = SimpleRouter()
router.register('titles', TitleViewSet)
# router.register('genres', GenreViewSet)
# router.register('categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet, basename='comment')

urlpatterns = [
    path(f'{API_VERSION}/', include('users.urls')),
    path(f'{API_VERSION}/', include(router.urls)),
    path(f'{API_VERSION}/genres/', GenreViewSet.as_view(
        {'get': 'list', 'post': 'create'})),
    path(f'{API_VERSION}/genres/<slug:slug>/', GenreViewSet.as_view(
        {'delete': 'destroy'})),
    path(f'{API_VERSION}/categories/', CategoryViewSet.as_view(
        {'get': 'list', 'post': 'create'})),
    path(f'{API_VERSION}/categories/<slug:slug>/', CategoryViewSet.as_view(
        {'delete': 'destroy'})),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # Временно
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),  # Временно
]
