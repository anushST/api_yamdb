"""Api app permissions."""
from rest_framework import permissions

from users.models import User


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow only author of object, moderator, admin or superuser."""

    def has_object_permission(self, request, view, obj):
        """Object permissions."""
        if (request.method in permissions.SAFE_METHODS
            or request.user.role == User.UsersType.MODERATOR
            or request.user.role == User.UsersType.ADMIN
           or request.user.is_superuser):
            return True

        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow only for admin or superuser."""

    def has_permission(self, request, view):
        """Object permissions."""
        return ((request.method in permissions.SAFE_METHODS)
                or (request.user.is_authenticated
                    and (request.user.role == User.UsersType.ADMIN
                         or request.user.is_superuser)))
