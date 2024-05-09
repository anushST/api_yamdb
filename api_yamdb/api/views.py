"""Views for api app."""
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Review, Title
from .filter import TitleFilter
from .mixins import HttpMethodsMixin
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class TitleViewSet(HttpMethodsMixin, viewsets.ModelViewSet):
    """ViewSet for Title model."""

    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """Return queryset of title object."""
        queryset = Title.objects.annotate(
            rating_avg=Avg('reviews__score')
        ).order_by('name')
        return queryset


class GenreViewSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, viewsets.GenericViewSet):
    """ViewSet for Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                      viewsets.GenericViewSet):
    """ViewSet for Category model."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class ReviewViewSet(HttpMethodsMixin, viewsets.ModelViewSet):
    """ViewSet for Review model."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_title(self):
        """Return title object."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        """Return queryset of title object."""
        title = self.get_title()
        return title.reviews.all().order_by('-pub_date')

    def perform_create(self, serializer):
        """Save serializer data."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(HttpMethodsMixin, viewsets.ModelViewSet):
    """ViewSet for Comment model."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_review(self):
        """Return review object."""
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id, title_id=title_id)

    def get_queryset(self):
        """Return queryset of review object."""
        review = self.get_review()
        return review.comments.all().order_by('-pub_date')

    def perform_create(self, serializer):
        """Save serializer data."""
        review = self.get_review()
        serializer.save(
            author=self.request.user,
            review=review
        )
