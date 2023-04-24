from django.db import models
from django.utils.html import mark_safe
from sorl.thumbnail import ImageField


# Create your models here.
class Entry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    common_name = models.CharField(max_length=50)
    species = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="images/")

    def img_preview(self):
        return mark_safe(f"<img src='{self.photo.url}' width='300' />")

    class Meta:
        verbose_name_plural = "entries"
