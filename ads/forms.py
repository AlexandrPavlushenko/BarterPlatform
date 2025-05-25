from django.core.validators import MaxLengthValidator

from .models import Ad, ExchangeProposal

from django import forms


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise forms.ValidationError("Заголовок не должен превышать 49 символов")
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 500:
            raise forms.ValidationError("Описание не должно превышать 199 символов")
        return description


class ExchangeProposalForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'style': 'border-radius: 10px; border: 1px solid #ced4da;',
            'placeholder': 'Опишите ваше предложение обмена...',
            'maxlength': '500'
        }),
        validators=[MaxLengthValidator(500)],
        required=True,
        error_messages={
            'required': 'Пожалуйста, напишите комментарий',
            'max_length': 'Комментарий не должен превышать 500 символов'
        }
    )

    class Meta:
        model = ExchangeProposal
        fields = ['comment']