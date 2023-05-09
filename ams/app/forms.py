from datetime import date
from django import forms
from django.db import models
from .models import Entry, FeedingSchedule, Note


class CreateForm(forms.ModelForm):
    current_year = date.today().year
    year_range = [x for x in range(current_year - 20, current_year + 1)]

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Name", "title": "Name"}
        ),
        label="",
        required=False,
    )
    common_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Common name",
                "title": "Common name",
            }
        ),
        label="",
    )
    species = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Species",
                "title": "Species",
            }
        ),
        label="",
    )
    sex = forms.ChoiceField(
        choices=(("MALE", "Male"), ("FEMALE", "Female"), ("UNKNOWN", "Unknown")),
        widget=forms.RadioSelect(
            attrs={"class": "d-inline-flex gap-5", "title": "Sex"}
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
                "title": "Date acquired",
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


class NoteForm(forms.ModelForm):
    text = forms.CharField(
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Add a note",
                "title": "Note",
                "rows": 4,
            }
        ),
        label="",
    )

    class Meta:
        model = Note
        fields = ["text"]


class ScheduleForm(forms.ModelForm):
    current_year = date.today().year
    year_range = [x for x in range(current_year - 20, current_year + 1)]

    food_type = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Food type",
                "title": "Food Type",
            }
        ),
        label="",
        required=True,
    )
    food_quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Food quantity",
                "title": "Food quantity",
            }
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
                "title": "Last fed date",
            }
        ),
        label="",
        required=True,
    )
    feed_interval = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Feed interval",
                "title": "Feed interval",
            }
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
                "title": "Next feed date",
            }
        ),
        label="",
        required=False,
    )

    class Meta:
        model = FeedingSchedule
        fields = "__all__"
