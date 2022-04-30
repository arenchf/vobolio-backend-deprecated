from django.db import models
from django.conf import settings


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    dictionary = models.ForeignKey("dictionary.Dictionary", on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)



class Word(models.Model):
    word = models.CharField(max_length=256)
    translation = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)
    dictionary = models.ForeignKey("dictionary.Dictionary", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)





