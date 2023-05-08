from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("entry/<int:id>", views.entry, name="entry"),
    path("create/", views.create, name="create"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("schedule/<int:id>", views.schedule, name="schedule"),
]
