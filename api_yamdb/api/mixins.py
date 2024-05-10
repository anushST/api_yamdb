"""Mixins for api app."""
from rest_framework import filters, viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)

from .permissions import IsAdminOrReadOnly


class HttpMethodsMixin:
    """Mixin for 'get', 'post', 'delete', 'patch' methods."""

    http_method_names = ['get', 'post', 'delete', 'patch']


class GenreCategoryMixin(CreateModelMixin, ListModelMixin,
                         DestroyModelMixin, viewsets.GenericViewSet):
    """Mixin for GenreViewSet and CategoryViewSet."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
