import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from ads.forms import AdForm, ExchangeProposalForm


@pytest.mark.django_db
class TestAdForm:
    def test_valid_form(self):
        form_data = {
            "title": "Test Ad",
            "description": "Test description",
            "category": "electronics",
            "condition": "new",
        }
        # Создаем корректное изображение
        from PIL import Image
        from io import BytesIO

        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        image_file = SimpleUploadedFile(
            "test.jpg", buffer.getvalue(), content_type="image/jpeg"
        )

        form = AdForm(data=form_data, files={"image": image_file})
        assert form.is_valid(), f"Form errors: {form.errors}"

    def test_title_max_length(self):
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
    def test_valid_form(self):
        form_data = {"comment": "Test comment"}
        form = ExchangeProposalForm(data=form_data)
        assert form.is_valid()

    def test_comment_required(self):
        form = ExchangeProposalForm(data={})
        assert not form.is_valid()
        assert "comment" in form.errors
