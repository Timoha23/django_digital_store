from django import forms


class RejectForm(forms.Form):
    reason = forms.CharField(
        max_length=512,
        required=True,
        widget=forms.Textarea,
    )
