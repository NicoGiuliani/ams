import datetime
from django.db import models
from django.utils.html import mark_safe
from sorl.thumbnail import ImageField


class Entry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    common_name = models.CharField(max_length=50)
    species = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    date_acquired = models.DateField()
    acquired_from = models.CharField(max_length=100)
    photo = ImageField(upload_to="images/", blank=True, null=True)

    def img_preview(self):
        return mark_safe(f"<img src='{self.photo.url}' width='300' />")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "entries"


class Note(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    belongs_to = models.ForeignKey(Entry, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=True, null=True)


class FeedingSchedule(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    belongs_to = models.OneToOneField(Entry, on_delete=models.CASCADE)
    food_type = models.CharField(max_length=50, blank=True, null=True)
    food_quantity = models.IntegerField(blank=True, null=True)
    last_fed_date = models.DateField(blank=True, null=True)
    feed_interval = models.IntegerField(blank=True, null=True)
    next_feed_date = models.DateField(blank=True, null=True)
