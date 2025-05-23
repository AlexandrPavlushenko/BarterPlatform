from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации нового пользователя"""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(forms.ModelForm):
    """Форма профиля пользователя"""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "city"
        )