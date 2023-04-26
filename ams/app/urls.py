from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("entry/<int:id>", views.entry, name="entry"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("create/", views.create, name="create"),
]
