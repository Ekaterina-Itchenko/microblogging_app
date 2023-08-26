from typing import Any

from django import forms


class SelectTagsForm(forms.Form):
    """An implementation form to select a tag."""

    tag = forms.ChoiceField(label="Choose a tag", required=False, widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, tags: list[tuple[str, str]], *args: Any, **kwargs: Any) -> None:
        super(SelectTagsForm, self).__init__(*args, **kwargs)
        self.fields["tag"].choices = tags
