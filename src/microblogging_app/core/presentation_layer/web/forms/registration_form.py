from core.presentation_layer.web.validators import ValidateUserAge
from django import forms


class RegistrationForm(forms.Form):
    """An implementation of registration form."""

    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(
        label="Username", strip=True, max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    birth_date = forms.DateField(
        label="Birth date",
        validators=[ValidateUserAge(min_age=18)],
        widget=forms.DateInput(attrs={"class": "form-control"}),
        help_text="Enter date of birth in following format: YYYY-MM-DD",
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
