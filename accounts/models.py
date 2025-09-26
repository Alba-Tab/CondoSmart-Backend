from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedBy

class CustomUser(AbstractUser,TimeStampedBy): 
    ci = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=24, blank=True)

    def __str__(self) -> str:  # útil en admin
        return f"{self.username} ({self.ci})"

