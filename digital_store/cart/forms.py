from django import forms

from .models import Cart


class CountItemsCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('count_items',)
