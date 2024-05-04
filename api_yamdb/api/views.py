from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .pagination import CustomPagination
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Title, Genre, Category, Review, User
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (TitleSerializer, GenreSerializer, CategorySerializer,
                          ReviewSerializer, CommentSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all().order_by('-pub_date')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get('title_id')
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id, title_id=title_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all().order_by('-pub_date')

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            author=self.request.user,
            review=review
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
