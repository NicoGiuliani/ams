from django.contrib import admin
from .models import Entry


class EntryAdmin(admin.ModelAdmin):
    readonly_fields = ["img_preview"]


# Register your models here.
admin.site.register(Entry, EntryAdmin)
