"""Permissions of users app."""
from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """Allow only admin and superuser."""

    def has_permission(self, request, view):
        """Check permission."""
        url = request.get_full_path()
        if '/me/' in url:
            return True
        return request.user.is_admin
