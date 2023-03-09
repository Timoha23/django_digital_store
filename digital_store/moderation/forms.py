from django import forms


class RejectForm(forms.Form):
    reason = forms.CharField(
        max_length=512,
        required=True,
        widget=forms.Textarea,
    )

    def clean_reason(self):
        reason = self.cleaned_data['reason']
        for word in reason.split():
            if len(word) > 20:
                raise forms.ValidationError('Длина одного слова не может превышать 20 символов.')
        return reason
