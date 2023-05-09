from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Entry, FeedingSchedule, Note
from .forms import CreateForm, NoteForm, ScheduleForm


# Create your views here.
def home(request):
    entries = Entry.objects.all()
    return render(request, "home.html", {"entries": entries})


def entry(request, id):
    print(f"The ID for this page is {id}")
    entry = Entry.objects.get(pk=id)
    return render(request, "entry.html", {"entry": entry})


def notes(request, id):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            try:
                entry = Entry.objects.get(pk=id)
            except:
                return redirect("home")

            new_text = form.cleaned_data["text"]
            new_note = Note(
                belongs_to=entry,
                text=new_text,
            )
            new_note.save()
            return redirect("notes", id)
    else:
        try:
            entry = Entry.objects.get(pk=id)
            notes = Note.objects.filter(belongs_to=entry)
            form = NoteForm
            return render(
                request, "notes.html", {"entry": entry, "notes": notes, "form": form}
            )
        except:
            print("Something went wrong")
            return redirect("home")


def edit(request, id):
    try:
        entry = Entry.objects.get(pk=id)
        if request.method == "POST":
            print("POST")
            form = CreateForm(request.POST, request.FILES, instance=entry)
            if form.is_valid():
                print("IT'S VALID")
                form.save()
                return redirect("home")
        else:
            form = CreateForm(
                instance=entry,
                initial={
                    "date_acquired": entry.date_acquired.strftime("%m/%d/%Y"),
                    "sex": entry.sex,
                },
            )
            return render(request, "create_form.html", {"form": form})
    except:
        print("Entry not found")
        return redirect("home")


def delete(request, id):
    entry = Entry.objects.get(pk=id)
    if request.method == "POST":
        if entry.feeding_schedule:
            feeding_schedule = FeedingSchedule.objects.get(pk=entry.feeding_schedule.id)
            feeding_schedule.delete()
        if entry.photo:
            entry.photo.delete()
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
            new_sex = form.cleaned_data["sex"]
            new_date_acquired = form.cleaned_data["date_acquired"]
            new_photo = form.cleaned_data["photo"]

            new_entry = Entry(
                name=new_name,
                common_name=new_common_name,
                species=new_species,
                sex=new_sex,
                photo=new_photo,
                date_acquired=new_date_acquired,
            )
            new_entry.save()
            # messages.success(request, "Entry has been saved successfully")
            print("IT'S BEEN SAVED")
            return redirect("home")
            # return render(
            #     request, "create_form.html", {"form": CreateForm, "success": True}
            # )
    else:
        print("GET")
        form = CreateForm()
    return render(request, "create_form.html", {"form": CreateForm})


def schedule(request, id):
    if request.method == "POST":
        print("POST")
        form = ScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            print("IT'S VALID")
            new_food_type = form.cleaned_data["food_type"]
            new_food_quantity = form.cleaned_data["food_quantity"]
            new_last_fed_date = form.cleaned_data["last_fed_date"]
            new_next_feed_date = form.cleaned_data["next_feed_date"]
            new_feed_interval = form.cleaned_data["feed_interval"]

            new_entry = FeedingSchedule(
                food_type=new_food_type,
                food_quantity=new_food_quantity,
                last_fed_date=new_last_fed_date,
                feed_interval=new_feed_interval,
                next_feed_date=new_next_feed_date,
            )
            new_entry.save()
            entry = Entry.objects.filter(id=id)
            entry.update(feeding_schedule=new_entry)
            messages.success(request, "Schedule has been saved successfully")
            print("IT'S BEEN SAVED")
            return redirect("entry", id)
    else:
        print("GET")
        entry = Entry.objects.get(pk=id)
        form = ScheduleForm
        if entry.feeding_schedule:
            form = ScheduleForm(
                instance=entry.feeding_schedule,
                initial={
                    "last_fed_date": entry.feeding_schedule.last_fed_date.strftime(
                        "%m/%d/%Y"
                    ),
                    "next_feed_date": entry.feeding_schedule.next_feed_date.strftime(
                        "%m/%d/%Y"
                    ),
                },
            )

        return render(request, "feeding_schedule.html", {"form": form, "entry": entry})


def delete_schedule(request, id):
    try:
        entry = Entry.objects.get(pk=id)
        feeding_schedule = entry.feeding_schedule
        feeding_schedule.delete()
    except:
        print("Schedule not found")
    return redirect("entry", id=id)
