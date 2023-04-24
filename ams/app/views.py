from django.shortcuts import render
from .models import Entry


# Create your views here.
def home(request):
    entries = Entry.objects.all()
    return render(request, "home.html", {"entries": entries})
