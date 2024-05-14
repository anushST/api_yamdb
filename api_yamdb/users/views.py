"""Views for users app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AllowOnlyAdminOrSuperuser
from .serializers import (
    ConfirmationCodeSerializer, SignupSerializer, UserSerializer)
from .send_mail import send_mail_to_user
from api.mixins import HttpMethodsMixin

User = get_user_model()


class UserViewSet(HttpMethodsMixin, ModelViewSet):
    """ViewSet for admin user to control User model."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AllowOnlyAdminOrSuperuser)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=('get', 'patch'),
            url_path='me', url_name='current_user',
            permission_classes=(IsAuthenticated,))
    def current_user(self, request):
        """Get current user."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
        else:
            serializer = UserSerializer(request.user, data=request.data,
                                        partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupAPIView(APIView):
    """APIView to signup the user."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Execute when POST method."""
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        code: str = default_token_generator.make_token(user)
        send_mail_to_user(user, code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenAPIView(APIView):
    """APIView to get JWT-token."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Execute when POST method."""
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username: str = serializer.data.get('username', None)
        user = get_object_or_404(User, username=username)
        refresh_token = RefreshToken.for_user(user)
        return Response({"token": str(refresh_token.access_token)},
                        status=status.HTTP_200_OK)
