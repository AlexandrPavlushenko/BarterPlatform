from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер пользователей для работы с email вместо username."""

    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет обычного пользователя с email и паролем.

        Args:
            email (str): Email адрес пользователя
            password (str, optional): Пароль пользователя. По умолчанию None.
            **extra_fields: Дополнительные поля пользователя.

        Returns:
            User: Созданный пользователь

        Raises:
            ValueError: Если email не был указан
        """
        if not email:
            raise ValueError("Пользователю необходимо указать адрес электронной почты")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя с email и паролем.

        Args:
            email (str): Email адрес суперпользователя
            password (str, optional): Пароль суперпользователя. По умолчанию None.
            **extra_fields: Дополнительные поля суперпользователя.

        Returns:
            User: Созданный суперпользователь

        Raises:
            ValueError: Если is_staff или is_superuser не установлены в True
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
