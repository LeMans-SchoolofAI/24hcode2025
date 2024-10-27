from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    api_key = models.CharField(max_length=100, unique=True, blank=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
