from django import forms
from core.presentation_layer.validators import ValidateUserAge


class RegistrationForm(forms.Form):
    """ An implementation of registration form."""

    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Enter username", strip=True, max_length=50)
    birth_date = forms.DateField(
        label="Enter date of birth in following format: YYYY-MM-DD",
        #input_formats="%Y-%m-%d",
        validators=[ValidateUserAge(min_age=18)]
    )
    password = forms.CharField(label="Enter a password", widget=forms.PasswordInput)
