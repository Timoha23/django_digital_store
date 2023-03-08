from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        widgets = {
            'text': forms.Textarea,
        }
        fields = ('text', 'rating')
