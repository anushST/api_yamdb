"""Api app permissions."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow only author of object, moderator, admin or superuser."""

    def has_object_permission(self, request, view, obj):
        """Object permissions."""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_moderator
                or request.user.is_admin
                or obj.author == request.user)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow only for admin or superuser."""

    def has_permission(self, request, view):
        """Object permissions."""
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))
