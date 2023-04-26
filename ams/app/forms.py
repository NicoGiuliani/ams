from django import forms
from django.db import models
from .models import Entry


class CreateForm(forms.Form):
    name = forms.CharField(max_length=50)
    common_name = forms.CharField(max_length=50)
    species = forms.CharField(max_length=100)
    photo = forms.ImageField(required=True)

    class Meta:
        model = Entry
        fields = "__all__"
