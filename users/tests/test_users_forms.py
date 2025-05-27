from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from users.forms import UserProfileForm, UserRegisterForm


@pytest.mark.django_db
class TestUserRegisterForm:
    def test_valid_form(self):
        """
        Тестирует валидность формы регистрации при корректных данных.

        Asserts:
            Форма должна быть валидной.
        """
        form_data = {
            "email": "test@example.com",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
        }
        form = UserRegisterForm(data=form_data)
        assert form.is_valid(), form.errors

    def test_password_mismatch(self):
        """
        Тестирует обработку ошибки несовпадающих паролей.

        Asserts:
            Форма невалидна, ошибка отмечена в поле password2, выводится ожидаемое сообщение об ошибке.
        """
        form_data = {
            "email": "register@example.com",
            "password1": "password123",
            "password2": "differentpassword",
        }
        form = UserRegisterForm(data=form_data)

        assert not form.is_valid()
        assert "password2" in form.errors
        assert "Введенные пароли не совпадают." in str(form.errors)

    def test_email_required(self):
        """
        Тестирует обязательность поля email.

        Asserts:
            Форма невалидна, ошибка отмечена в поле email.
        """
        form_data = {"email": "", "password1": "test123", "password2": "test123"}
        form = UserRegisterForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors


@pytest.mark.django_db
class TestUserProfileForm:
    def create_test_image(self):
        """
        Создаёт корректное тестовое изображение для загрузки в форму профиля.

        Returns:
            SimpleUploadedFile: JPEG-файл изображения для тестов.
        """
        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return SimpleUploadedFile(
            "test.jpg", buffer.getvalue(), content_type="image/jpeg"
        )

    def test_valid_form(self, test_user):
        """
        Тестирует валидность формы профиля с загрузкой аватара.

        Args:
            test_user (User): Тестовый пользователь.

        Asserts:
            Форма должна быть валидной.
        """
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "city": "New York",
        }
        form = UserProfileForm(
            data=form_data,
            files={"avatar": self.create_test_image()},
            instance=test_user,
        )
        assert form.is_valid(), form.errors

    def test_valid_form_without_avatar(self, test_user):
        """
        Тестирует валидность формы профиля без загрузки аватара.

        Args:
            test_user (User): Тестовый пользователь.

        Asserts:
            Форма должна быть валидной.
        """
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "city": "New York",
        }
        form = UserProfileForm(data=form_data, instance=test_user)
        assert form.is_valid(), form.errors

    def test_optional_fields(self, test_user):
        """
        Тестирует валидность формы профиля при пустых (необязательных) полях.

        Args:
            test_user (User): Тестовый пользователь.

        Asserts:
            Форма должна быть валидной.
        """
        form_data = {"first_name": "", "last_name": "", "phone": "", "city": ""}
        form = UserProfileForm(data=form_data, instance=test_user)
        assert form.is_valid(), form.errors
