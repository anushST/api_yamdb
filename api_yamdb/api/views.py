"""Views for api app."""
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Review, Title
from .filter import TitleFilter
from .mixins import HttpMethodsMixin, GenreCategoryMixin
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class TitleViewSet(HttpMethodsMixin, viewsets.ModelViewSet):
    """ViewSet for Title model."""

    queryset = queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')

    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(GenreCategoryMixin):
    """ViewSet for Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryMixin):
    """ViewSet for Category model."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
        return title.reviews.all()

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
        return review.comments.all()

    def perform_create(self, serializer):
        """Save serializer data."""
        review = self.get_review()
        serializer.save(
            author=self.request.user,
            review=review
        )
