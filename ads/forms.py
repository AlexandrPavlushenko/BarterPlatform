from django import forms
from django.core.validators import MaxLengthValidator

from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    """Форма для создания и редактирования объявлений.

    Attributes:
        Meta: Вложенный класс для базовой конфигурации формы
            - model: Модель Ad
            - fields: Поля для отображения в форме
            - widgets: Кастомизация виджетов полей

    Methods:
        clean_title: Валидация заголовка объявления
        clean_description: Валидация описания объявления
    """

    class Meta:
        model = Ad
        fields = ["title", "description", "image", "category", "condition"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 10}),
        }

    def clean_title(self):
        """Валидация поля заголовка.

        Returns:
            str: Очищенное значение заголовка

        Raises:
            forms.ValidationError: Если заголовок длиннее 100 символов
        """
        title = self.cleaned_data["title"]
        if len(title) > 100:
            raise forms.ValidationError("Заголовок не должен превышать 100 символов")
        return title

    def clean_description(self):
        """Валидация поля описания.

        Returns:
            str: Очищенное значение описания

        Raises:
            forms.ValidationError: Если описание длиннее 500 символов
        """
        description = self.cleaned_data["description"]
        if len(description) > 500:
            raise forms.ValidationError("Описание не должно превышать 500 символов")
        return description


class ExchangeProposalForm(forms.ModelForm):
    """Форма для создания предложений обмена.

    Attributes:
        comment: Кастомизированное поле комментария с:
            - Стилизованным Textarea
            - Валидацией максимальной длины
            - Кастомными сообщениями об ошибках
            - Плейсхолдером

        Meta: Вложенный класс для базовой конфигурации формы
            - model: Модель ExchangeProposal
            - fields: Поля для отображения в форме
    """

    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 10,
                "style": "border-radius: 20px; border: 1px solid #ced4da;",
                "placeholder": "Опишите ваше предложение обмена...",
                "maxlength": "500",
            }
        ),
        validators=[MaxLengthValidator(500)],
        required=True,
        error_messages={
            "required": "Пожалуйста, напишите комментарий",
            "max_length": "Комментарий не должен превышать 500 символов",
        },
    )

    class Meta:
        model = ExchangeProposal
        fields = ["comment"]
