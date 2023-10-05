from core.presentation_layer.common.validators import ValidateMaxTagCount
from core.presentation_layer.web.validators import WebValidator
from django import forms


class AddTweetForm(forms.Form):
    """An implementation of adding tweet form."""

    content = forms.CharField(max_length=400, label="Content", widget=forms.Textarea(attrs={"class": "form-control"}))
    tags = forms.CharField(
        max_length=100,
        label="Tags",
        validators=[WebValidator(ValidateMaxTagCount(max_count=20))],
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False,
        help_text="Enter the tags separated by a space or each from a new line. You can add only 20 tags.",
    )


class EditTweetForm(forms.Form):
    """An implementation of adding tweet form."""

    content = forms.CharField(max_length=400, label="Content", widget=forms.Textarea(attrs={"class": "form-control"}))
    tags = forms.CharField(
        max_length=100,
        label="Tags",
        validators=[WebValidator(ValidateMaxTagCount(max_count=20))],
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False,
        help_text="Enter the tags separated by a space or each from a new line. You can add only 20 tags.",
    )
    tweet_id = forms.IntegerField(widget=forms.HiddenInput, label="")
