from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации новых пользователей.

    Наследует стандартную UserCreationForm и адаптирует ее:
    - Использует email вместо username как идентификатор
    - Включает обязательные поля для пароля и его подтверждения

    Поля формы:
        email (EmailField): Электронная почта (используется как логин)
        password1 (CharField): Основной пароль
        password2 (CharField): Подтверждение пароля

    Методы:
        save: Создает нового пользователя с хешированием пароля
    """

    class Meta:
        model = User
        fields = ("email", "password1", "password2")  # Поля для регистрации


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя.

    Позволяет изменять персональные данные:
    - Основную информацию (имя, фамилия)
    - Контактные данные (телефон, город)
    - Аватар профиля

    Поля формы:
        first_name (CharField): Имя пользователя
        last_name (CharField): Фамилия пользователя
        phone (CharField): Номер телефона (необязательное)
        avatar (ImageField): Фото профиля
        city (CharField): Город проживания

    Особенности:
        - Все поля необязательные (required=False можно добавить в widgets)
        - Поддерживает валидацию телефонных номеров
        - Обрабатывает загрузку изображений
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone", "avatar", "city")  # Поля профиля
