from django import forms

from .models import Release


class SelectReleaseForm(forms.Form):
    release = forms.ModelChoiceField(
        queryset=Release.objects.all(),
        to_field_name="number",
        label="Release",
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
