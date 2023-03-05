from django import forms

from .models import Shop, Product, Item


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        widgets = {
            'description': forms.Textarea,
        }
        fields = ('name', 'image', 'description')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'image', 'description', 'visibile')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        widgets = {
            'item': forms.Textarea,
        }
        fields = ('item',)
