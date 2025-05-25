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


class ProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_receiver', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 10}),
        }
