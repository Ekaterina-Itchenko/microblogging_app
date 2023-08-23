from core.presentation_layer.validators import TagsNumberValidator
from django import forms


class TweetForm(forms.Form):
    """An implementation of a tweet (reply of a tweet) form."""

    content = forms.CharField(label="Content", widget=forms.Textarea, max_length=400)
    tags = forms.CharField(label="Tags", widget=forms.Textarea, validators=[TagsNumberValidator(max_number=5)])
