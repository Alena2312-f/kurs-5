from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer, UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    Представление для регистрации пользователя.
    """

    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Разрешить доступ всем


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Представление для получения JWT токена с использованием кастомного сериализатора.
    """

    serializer_class = MyTokenObtainPairSerializer
