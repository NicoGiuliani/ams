from datetime import date
from django import forms
from django.db import models
from .models import Entry, FeedingSchedule


class CreateForm(forms.ModelForm):
    current_year = date.today().year
    year_range = [x for x in range(current_year - 20, current_year + 1)]

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
        label="",
        required=False,
    )
    common_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Common name"}
        ),
        label="",
    )
    species = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Species"}
        ),
        label="",
    )
    date_acquired = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Date acquired",
                "onfocus": "(this.type='date')",
                "onblur": "if (this.value === '') { (this.type='text') }",
            }
        ),
        label="",
    )
    photo = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}),
        label="",
        required=False,
    )

    class Meta:
        model = Entry
        fields = ["name", "common_name", "species", "date_acquired", "photo"]


class ScheduleForm(forms.ModelForm):
    current_year = date.today().year
    year_range = [x for x in range(current_year - 20, current_year + 1)]

    food_type = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Food type"}
        ),
        label="",
        required=True,
    )
    food_quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Food quantity"}
        ),
        label="",
        required=True,
    )
    last_fed_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Last fed date",
                "onfocus": "(this.type='date')",
                "onblur": "if (this.value === '') { (this.type='text') }",
            }
        ),
        label="",
        required=True,
    )
    feed_interval = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Feed interval"}
        ),
        label="",
        required=True,
    )
    next_feed_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Next feed date",
                "onfocus": "(this.type='date')",
                "onblur": "if (this.value === '') { (this.type='text') }",
            }
        ),
        label="",
        required=False,
    )

    class Meta:
        model = FeedingSchedule
        fields = "__all__"
