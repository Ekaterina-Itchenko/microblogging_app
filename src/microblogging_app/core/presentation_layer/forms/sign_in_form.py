from django import forms


class SignInForm(forms.Form):
    """ An implementation of sign in form."""

    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Enter a password", widget=forms.PasswordInput)
