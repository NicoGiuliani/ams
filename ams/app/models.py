import datetime
from django.db import models
from django.utils.html import mark_safe
from sorl.thumbnail import ImageField


# Create your models here.
class FeedingSchedule(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    food_type = models.CharField(max_length=50, blank=True, null=True)
    food_quantity = models.IntegerField(blank=True, null=True)
    last_fed_date = models.DateField(blank=True, null=True)
    feed_interval = models.IntegerField(blank=True, null=True)
    next_feed_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.feed_interval and self.next_feed_date is None:
            self.next_feed_date = self.last_fed_date + datetime.timedelta(
                days=self.feed_interval
            )
        super(FeedingSchedule, self).save(*args, **kwargs)


class Entry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    common_name = models.CharField(max_length=50)
    species = models.CharField(max_length=100)
    date_acquired = models.DateField()
    photo = ImageField(upload_to="images/", blank=True, null=True)
    feeding_schedule = models.OneToOneField(
        FeedingSchedule, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def img_preview(self):
        return mark_safe(f"<img src='{self.photo.url}' width='300' />")

    class Meta:
        verbose_name_plural = "entries"
