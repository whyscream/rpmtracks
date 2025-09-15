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


class SearchTracksForm(forms.Form):
    query = forms.CharField(
        label="Search tracks",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter track artist or title"}),
    )
