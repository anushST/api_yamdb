"""Permissions of users app."""
from rest_framework import permissions


class AllowOnlyAdminAndSuperuser(permissions.BasePermission):
    """Allow only admin and superuser."""

    def has_permission(self, request, view):
        """Check permission."""
        return True if (request.user.is_authenticated
                        and (request.user.role == 'admin'
                             or request.user.is_superuser)) else False
