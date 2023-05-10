import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import Entry, FeedingSchedule, Note
from .forms import CreateForm, NoteForm, ScheduleForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def home(request):
    entries = Entry.objects.all()
    return render(request, "home.html", {"entries": entries})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        # print(form)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            return redirect("home")
        else:
            print(form.errors)
            return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": RegistrationForm})


@login_required
def entry(request, id):
    print(f"The ID for this page is {id}")
    entry = Entry.objects.get(pk=id)
    feeding_schedule = FeedingSchedule.objects.filter(belongs_to=entry)
    if len(feeding_schedule) > 0:
        feeding_schedule = feeding_schedule[0]
    # print(feeding_schedule)
    return render(
        request, "entry.html", {"entry": entry, "feeding_schedule": feeding_schedule}
    )


@login_required
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


@login_required
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
            return render(request, "create_form.html", {"form": form, "id": id})
    except:
        print("Entry not found")
        return redirect("home")


@login_required
def delete(request, id):
    entry = Entry.objects.get(pk=id)
    if request.method == "POST":
        if entry.photo:
            entry.photo.delete()
        entry.delete()
        return redirect("home")
    else:
        return render(request, "delete.html", {"entry": entry})


@login_required
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
            new_acquired_from = form.cleaned_data["acquired_from"]
            new_photo = form.cleaned_data["photo"]
            print(new_photo)

            new_entry = Entry(
                name=new_name,
                common_name=new_common_name,
                species=new_species,
                sex=new_sex,
                photo=new_photo,
                date_acquired=new_date_acquired,
                acquired_from=new_acquired_from,
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


@login_required
def search(request):
    if "query" in request.GET:
        query = request.GET["query"]
        search_results = Entry.objects.filter(
            Q(name__icontains=query)
            | Q(common_name__icontains=query)
            | Q(species__icontains=query)
            | Q(sex__iexact=query)
            | Q(date_acquired__icontains=query)
        )
        return render(request, "search.html", {"entries": search_results})


@login_required
def schedule(request, id):
    if request.method == "POST":
        print("POST")
        form = ScheduleForm(request.POST)
        if form.is_valid():
            print("IT'S VALID")
            try:
                entry = Entry.objects.get(pk=id)
            except:
                print("Something didn't work")
                return redirect("home")

            new_food_type = form.cleaned_data["food_type"]
            new_food_quantity = form.cleaned_data["food_quantity"]
            new_last_fed_date = form.cleaned_data["last_fed_date"]
            new_feed_interval = form.cleaned_data["feed_interval"]
            new_next_feed_date = form.cleaned_data["next_feed_date"]

            if new_feed_interval and new_next_feed_date is None:
                new_next_feed_date = new_last_fed_date + datetime.timedelta(
                    days=new_feed_interval
                )

            feeding_schedule = FeedingSchedule.objects.filter(belongs_to=entry)
            if len(feeding_schedule) > 0:
                feeding_schedule.update(
                    food_type=new_food_type,
                    food_quantity=new_food_quantity,
                    last_fed_date=new_last_fed_date,
                    feed_interval=new_feed_interval,
                    next_feed_date=new_next_feed_date,
                )
                print("updated")
            else:
                new_feeding_schedule = FeedingSchedule(
                    belongs_to=entry,
                    food_type=new_food_type,
                    food_quantity=new_food_quantity,
                    last_fed_date=new_last_fed_date,
                    feed_interval=new_feed_interval,
                    next_feed_date=new_next_feed_date,
                )
                new_feeding_schedule.save()
                messages.success(request, "Schedule has been saved successfully")
                print("IT'S BEEN SAVED")
            return redirect("entry", id)
    else:
        print("GET")
        form = ScheduleForm
        try:
            entry = Entry.objects.get(pk=id)
        except:
            print("Something didn't work")
            return redirect("home")
        feeding_schedule = FeedingSchedule.objects.filter(belongs_to=entry)
        if len(feeding_schedule) > 0:
            feeding_schedule = feeding_schedule[0]
            form = ScheduleForm(
                instance=feeding_schedule,
                initial={
                    "last_fed_date": feeding_schedule.last_fed_date.strftime(
                        "%m/%d/%Y"
                    ),
                    # "feed_interval": None,
                    "next_feed_date": None,
                },
            )

        return render(request, "feeding_schedule.html", {"form": form, "entry": entry})


@login_required
def delete_schedule(request, id):
    try:
        entry = Entry.objects.get(pk=id)
        feeding_schedule = FeedingSchedule.objects.get(belongs_to=entry)
        feeding_schedule.delete()
    except:
        print("Schedule not found")
    return redirect("entry", id=id)


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")
