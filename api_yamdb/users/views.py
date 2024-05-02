"""Views for users app."""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import SignupSerializer, UserSerializer

User = get_user_model()


class UserViewSetForAdmin(ModelViewSet):
    """ViewSet for admin user to control User model."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
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

        Overrided to allow only for admin and superuser.
        """
        super().check_permissions(request)
        if request.user.role != 'admin' or not request.user.is_superuser:
            raise PermissionDenied('Нет прав доступа')


class UserApiView(APIView):
    """APIView for users to control themselfs."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Execute when GET method."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Execute when PATCH method."""
        data = request.data.copy()
        data.pop('role', None)
        serializer = UserSerializer(request.user, data=data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupAPIView(APIView):
    """APIView to signup the user."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Execute when post method."""
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # ToDo email_sending
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenAPIView(APIView):
    """APIView to get JWT-token."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Execute when post method."""
        pass  # ToDo email_processing
