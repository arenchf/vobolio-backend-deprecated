from django.db import models
from django.conf import settings
# Create your models here.


class Dictionary(models.Model):
    language = models.CharField(max_length=10)
    name = models.CharField(max_length=256)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)
