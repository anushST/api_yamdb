"""Api app permissions."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow only author of object, moderator, admin or superuser."""

    def has_object_permission(self, request, view, obj):
        """Object permissions."""
        if (request.method in permissions.SAFE_METHODS
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
           or request.user.is_superuser):
            return True

        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow only for admin or superuser."""

    def has_permission(self, request, view):
        """Object permissions."""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return (
                request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))
