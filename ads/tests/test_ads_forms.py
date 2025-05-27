import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from ads.forms import AdForm, ExchangeProposalForm


@pytest.mark.django_db
class TestAdForm:
    """Тестирование формы создания/редактирования объявления (AdForm)."""

    def test_valid_form(self):
        """Проверяет валидность формы с корректными данными и изображением.

        Asserts:
            - Форма с корректными данными и изображением проходит валидацию
            - Нет ошибок валидации (form.errors пуст)
        """
        form_data = {
            "title": "Test Ad",
            "description": "Test description",
            "category": "electronics",
            "condition": "new",
        }
        # Создаем корректное изображение
        from io import BytesIO

        from PIL import Image

        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        image_file = SimpleUploadedFile(
            "test.jpg", buffer.getvalue(), content_type="image/jpeg"
        )

        form = AdForm(data=form_data, files={"image": image_file})
        assert form.is_valid(), f"Form errors: {form.errors}"

    def test_title_max_length(self):
        """Проверяет валидацию максимальной длины заголовка объявления.

        Asserts:
            - Форма с заголовком длинее 100 символов невалидна
            - В ошибках формы присутствует поле 'title'
        """
        form_data = {
            "title": "T" * 101,
            "description": "Test",
            "category": "electronics",
            "condition": "new",
        }
        form = AdForm(data=form_data)
        assert not form.is_valid()
        assert "title" in form.errors


@pytest.mark.django_db
class TestExchangeProposalForm:
    """Тестирование формы предложения обмена (ExchangeProposalForm)."""

    def test_valid_form(self):
        """Проверяет валидность формы с корректным комментарием.

        Asserts:
            - Форма с заполненным комментарием проходит валидацию
        """
        form_data = {"comment": "Test comment"}
        form = ExchangeProposalForm(data=form_data)
        assert form.is_valid()

    def test_comment_required(self):
        """Проверяет обязательность поля комментария.

        Asserts:
            - Форма без комментария невалидна
            - В ошибках формы присутствует поле 'comment'
        """
        form = ExchangeProposalForm(data={})
        assert not form.is_valid()
        assert "comment" in form.errors
