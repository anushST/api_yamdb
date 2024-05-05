"""Pagination classes for api app."""
from rest_framework.pagination import PageNumberPagination

from .constants import PAGE_SIZE


class CustomPagination(PageNumberPagination):
    """Custom pagination class."""

    page_size = PAGE_SIZE
