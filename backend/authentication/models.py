from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=64)
    is_visible = models.BooleanField(default=True)


class CustomUser(AbstractUser):
    main_language = models.CharField(blank=True, max_length=120)
    roles = models.ManyToManyField(Role)

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()
