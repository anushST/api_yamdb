"""Views for users app."""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer

User = get_user_model()


class UserViewSetForAdmin(ModelViewSet):
    """ViewSet for admin user to control User model."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        """Update data in database.

        Overrided to allow only PATCH method.
        """
        if request.method == 'PATCH':
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def check_permissions(self, request):
        """Check if the request should be permitted.

        Overrided to check that is the user admin.
        """
        super().check_permissions(request)
        if request.user.role != 'admin':
            raise PermissionDenied('Нет прав доступа')


class UserApiView(APIView):
    """APIView for users to control themselfs."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Execute GET method."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Execute PATCH method."""
        data = request.data.copy()
        data.pop('role', None)
        serializer = UserSerializer(request.user, data=data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
