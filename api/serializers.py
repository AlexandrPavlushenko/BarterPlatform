from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения пары токенов (доступ и обновление),
    добавляет дополнительные данные пользователя в токен."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя.
    Позволяет создавать нового пользователя и управлять паролем."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User(
            first_name=validated_data.get("first_name", None),
            last_name=validated_data.get("last_name", None),
            email=validated_data["email"],
            phone=validated_data.get("phone", None),
            avatar=validated_data.get("avatar", None),
            city=validated_data.get("city", None),
        )
        # Устанавливаем пароль пользователя
        user.set_password(validated_data["password"])
        user.save()
        return user
