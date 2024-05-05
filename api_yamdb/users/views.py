"""Views for users app."""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AllowOnlyAdminOrSuperuser
from .serializers import (
    ConfirmationCodeSerializer, SignupSerializer, UserSerializer)
from .send_mail import check_code, send_mail_to_user

User = get_user_model()


class UserViewSetForAdmin(ModelViewSet):
    """ViewSet for admin user to control User model."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AllowOnlyAdminOrSuperuser,)
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


class UserApiView(APIView):
    """APIView for users to control themselfs."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Execute when GET method."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """Execute when PATCH method."""
        data = request.data.copy()
        data.pop('role', None)
        serializer = UserSerializer(request.user, data=data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupAPIView(APIView):
    """APIView to signup the user."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Execute when POST method."""
        serializer = SignupSerializer(data=request.data)
        username = serializer.initial_data.get('username', None)
        email = serializer.initial_data.get('email', None)
        try:
            user = User.objects.get(username=username, email=email)
            send_mail_to_user(user)
            return Response(serializer.initial_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            if serializer.is_valid():
                user = serializer.save()
                send_mail_to_user(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenAPIView(APIView):
    """APIView to get JWT-token."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Execute when POST method."""
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                username: str = serializer.data.get('username', None)
                user = User.objects.get(username=username)
                confirmation_code: int = serializer.data.get(
                    'confirmation_code', None)
                if check_code(user, confirmation_code):
                    refresh_token = RefreshToken.for_user(user)
                    return Response({"token": str(refresh_token.access_token)},
                                    status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "Пользователь не найден"},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"message": "Отсутствует обязательное поле или оно некорректно"},
            status=status.HTTP_400_BAD_REQUEST)
