from django.shortcuts import render
from .models import Entry
from .forms import CreateForm


# Create your views here.
def home(request):
    entries = Entry.objects.all()
    return render(request, "home.html", {"entries": entries})


def entry(request, id):
    print(f"The ID for this page is {id}")
    entry = Entry.objects.get(pk=id)
    return render(request, "entry.html", {"entry": entry})


def create(request):
    return render(request, "create_form.html", {"form": CreateForm})
