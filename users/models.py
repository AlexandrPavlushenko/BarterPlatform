from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Эл.почта")
    first_name = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Фамилия"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"