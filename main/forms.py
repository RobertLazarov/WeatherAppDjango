from django import forms


class CityForm(forms.Form):
    city = forms.CharField(
    max_length=80,
    label='City',
    widget=forms.TextInput(attrs={
    'placeholder': 'e.g., Bucharest',
    'autofocus': 'autofocus'
    }),
    )