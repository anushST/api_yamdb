"""Mixins for api app."""


class HttpMethodsMixin:
    """Mixin for 'get', 'post', 'delete', 'patch' methods."""

    http_method_names = ['get', 'post', 'delete', 'patch']
