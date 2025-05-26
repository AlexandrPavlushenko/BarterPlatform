import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from users.forms import UserRegisterForm, UserProfileForm
from PIL import Image
from io import BytesIO


@pytest.mark.django_db
class TestUserRegisterForm:
    def test_valid_form(self):
        """Тест валидной формы регистрации"""
        form_data = {
            "email": "test@example.com",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
        }
        form = UserRegisterForm(data=form_data)
        assert form.is_valid(), form.errors

    def test_password_mismatch(self):
        """Тест несовпадающих паролей"""
        form_data = {
            "email": "register@example.com",
            "password1": "password123",
            "password2": "differentpassword",
        }
        form = UserRegisterForm(data=form_data)

        # Проверяем что форма невалидна
        assert not form.is_valid()
        # Проверяем что ошибка в поле password2
        assert "password2" in form.errors
        # Проверяем конкретное сообщение об ошибке
        assert "Введенные пароли не совпадают." in str(form.errors)

    def test_email_required(self):
        """Тест обязательности email"""
        form_data = {"email": "", "password1": "test123", "password2": "test123"}
        form = UserRegisterForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors


@pytest.mark.django_db
class TestUserProfileForm:
    def create_test_image(self):
        """Создает корректное тестовое изображение"""
        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return SimpleUploadedFile(
            "test.jpg", buffer.getvalue(), content_type="image/jpeg"
        )

    def test_valid_form(self, test_user):
        """Тест валидной формы профиля с аватаром"""
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
        """Тест формы без аватара"""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "city": "New York",
        }
        form = UserProfileForm(data=form_data, instance=test_user)
        assert form.is_valid(), form.errors

    def test_optional_fields(self, test_user):
        """Тест необязательных полей"""
        form_data = {"first_name": "", "last_name": "", "phone": "", "city": ""}
        form = UserProfileForm(data=form_data, instance=test_user)
        assert form.is_valid(), form.errors
