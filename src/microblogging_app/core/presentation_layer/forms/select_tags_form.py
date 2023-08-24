from core.business_logic.services import get_tags
from django import forms


class SelectTagsForm(forms.Form):
    """An implementation form to select a tag."""

    tag = forms.ChoiceField(label="Choose a tag", choices=get_tags())
