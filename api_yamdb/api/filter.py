"""Custom Api filters."""
import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Custom filter for TitleSerializer."""

    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='iexact')
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact')

    class Meta:
        """Meta-data of TitleFilter."""

        model = Title
        fields = ['name', 'year', 'genre', 'category']
