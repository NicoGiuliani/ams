from django.shortcuts import redirect, render
from django.contrib import messages
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


def delete(request, id):
    entry = Entry.objects.get(pk=id)
    if request.method == "POST":
        entry.delete()
        return redirect("home")
    else:
        return render(request, "delete.html", {"entry": entry})


def create(request):
    if request.method == "POST":
        print("POST")
        form = CreateForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            print("IT'S VALID")
            new_name = form.cleaned_data["name"]
            new_common_name = form.cleaned_data["common_name"]
            new_species = form.cleaned_data["species"]
            new_photo = form.cleaned_data["photo"]

            new_entry = Entry(
                name=new_name,
                common_name=new_common_name,
                species=new_species,
                photo=new_photo,
            )
            new_entry.save()
            messages.success(request, "Entry has been saved successfully")
            print("IT'S BEEN SAVED")
            return render(
                request, "create_form.html", {"form": CreateForm, "success": True}
            )
    else:
        print("GET")
        form = CreateForm()
    return render(request, "create_form.html", {"form": CreateForm})
