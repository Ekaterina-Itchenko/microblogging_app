from django import forms


class SelectTagsForm(forms.Form):
    """An implementation form to select a tag."""

    tag = forms.CharField(label="Choose a tag", required=False, max_length=50,
                          widget=forms.TextInput(attrs={"class": "form-control"}))
