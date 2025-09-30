from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedBy

class CustomUser(AbstractUser,TimeStampedBy): 
    ci = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=24, blank=True)
    photo_key = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self) -> str:  # útil en admin
        estado= "" if self.is_active else "INACTIVO"
        return f"{self.username} ({self.ci}) [{estado}]"

