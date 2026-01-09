from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    password = serializers.CharField(write_only=True)
    tg_chat_id = serializers.CharField(required=False)  # Добавляем поле tg_chat_id

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "tg_chat_id",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        tg_chat_id = validated_data.pop("tg_chat_id", None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        if tg_chat_id is not None:
            user.tg_chat_id = tg_chat_id
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Сериализатор для получения JWT токена.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token["username"] = user.username
        token["email"] = user.email
        token["tg_chat_id"] = user.tg_chat_id

        return token
