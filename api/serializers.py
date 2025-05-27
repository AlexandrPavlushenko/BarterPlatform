from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ads.models import Ad, ExchangeProposal

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный сериализатор JWT-токенов с дополнительными полями пользователя.

    Наследует стандартный сериализатор токенов и добавляет в токен:
    - email пользователя
    - Имя (first_name)
    - Фамилию (last_name)

    Используется для:
    - Генерации access/refresh токенов
    - Передачи базовой информации о пользователе в токене
    """

    @classmethod
    def get_token(cls, user):
        """Генерирует токен с дополнительными пользовательскими данными.

        Args:
            user: Объект пользователя Django

        Returns:
            Token: JWT-токен с доп. полями
        """
        token = super().get_token(user)
        token["email"] = user.email
        token["first_name"] = user.first_name or ""
        token["last_name"] = user.last_name or ""
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации новых пользователей.

    Обрабатывает:
    - Валидацию паролей (проверка совпадения)
    - Создание нового пользователя
    - Обработку дополнительных необязательных полей

    Поля:
    - Обязательные: email, password, password2
    - Необязательные: first_name, last_name, phone, avatar, city
    """

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "city",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "phone": {"required": False},
            "avatar": {"required": False},
            "city": {"required": False},
        }

    def validate(self, attrs):
        """Проверяет совпадение паролей."""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        """Создает нового пользователя, удаляя подтверждение пароля."""
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения информации о пользователе.

    Используется для:
    - Отображения профиля пользователя
    - Вложенного отображения в других сериализаторах

    Поля только для чтения:
    - id
    - email
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "avatar", "city"]
        read_only_fields = ["id", "email"]


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор для объявлений.

    Включает:
    - Вложенную информацию об авторе (UserSerializer)
    - Обработку изображений (необязательное поле)
    - Автоматическую установку автора при создании

    Поля только для чтения:
    - id
    - author
    - created_at
    - updated_at
    """

    author = UserSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "author",
            "title",
            "description",
            "image",
            "category",
            "condition",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]


class ExchangeProposalSerializer(serializers.ModelSerializer):
    """Сериализатор для предложений обмена.

    Включает:
    - Вложенную информацию об отправителе, получателе и объявлении
    - Поля только для чтения (кроме комментария)

    Используется для:
    - Просмотра предложений
    - Создания новых предложений (только с комментарием)
    """

    ad_sender = UserSerializer(read_only=True)
    receiver_user = UserSerializer(read_only=True)
    ad = AdSerializer(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = [
            "id",
            "ad_sender",
            "receiver_user",
            "ad",
            "comment",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "ad_sender",
            "receiver_user",
            "ad",
            "status",
            "created_at",
        ]


class ExchangeProposalUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления статуса предложения обмена.

    Используется исключительно для:
    - Изменения статуса предложения (принято/отклонено)
    - Доступно только владельцу объявления

    Разрешенные статусы определяются моделью ExchangeProposal.
    """

    class Meta:
        model = ExchangeProposal
        fields = ["status"]
