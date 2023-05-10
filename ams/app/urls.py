from django.conf import settings
from django.urls import path, include
from . import views
from .forms import UserLoginForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("entry/<int:id>", views.entry, name="entry"),
    path("notes/<int:id>", views.notes, name="notes"),
    path("create/", views.create, name="create"),
    path("register/", views.register, name="register"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("schedule/<int:id>", views.schedule, name="schedule"),
    path("delete_schedule/<int:id>", views.delete_schedule, name="delete_schedule"),
    path("search/", views.search, name="search"),
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),
    path(
        "accounts/login",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm,
        ),
        name="login",
    ),
    path(
        "accounts/logout",
        views.custom_logout,
        name="logout",
    ),
]
