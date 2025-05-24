from django import forms
from .models import Ad, ExchangeProposal

from django import forms
from .models import Ad

from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
        }

class ProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_receiver', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 10}),
        }