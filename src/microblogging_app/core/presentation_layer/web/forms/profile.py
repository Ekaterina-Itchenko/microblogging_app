from typing import Any

from core.presentation_layer.common.validators import (
    ValidateFileSize,
    ValidateImageExtensions,
    ValidateUserAge,
)
from core.presentation_layer.web.validators import WebValidator
from django import forms


class EditProfileForm(forms.Form):
    """An implementation of edit profile form."""

    photo = forms.ImageField(
        label="Photo",
        allow_empty_file=False,
        required=False,
        validators=[
            WebValidator(ValidateImageExtensions(["png", "jpeg", "jpg"])),
            WebValidator(ValidateFileSize(max_size=5_000_000)),
        ],
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="First name",
        strip=True,
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last name",
        strip=True,
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        strip=True,
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}), required=True)
    birth_date = forms.DateField(
        label="Date of birth",
        help_text="Enter date of birth in following format: YYYY-MM-DD",
        validators=[WebValidator(ValidateUserAge(min_age=18))],
        widget=forms.DateInput(attrs={"class": "form-control"}),
        required=True,
    )
    description = forms.CharField(
        label="Description",
        strip=True,
        max_length=400,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    country = forms.ChoiceField(label="Country", required=True, widget=forms.Select(attrs={"class": "form-control"}))
    old_password = forms.CharField(
        label="Old password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        help_text="To change your password, you need to enter the old valid password.",
    )
    new_password = forms.CharField(
        label="New password", widget=forms.PasswordInput(attrs={"class": "form-control"}), required=False
    )
    user_id = forms.IntegerField(widget=forms.HiddenInput, label="")
    old_email = forms.EmailField(widget=forms.HiddenInput, label="")

    def __init__(self, countries: list[tuple[str, str]], *args: Any, **kwargs: Any) -> None:
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["country"].choices = countries
