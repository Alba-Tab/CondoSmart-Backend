from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedBy


class Rol(TimeStampedBy): # ya hereda models.Model de TimeStampedBy
    GROUPS = [("admin","administrador"),("guard","guardia"),("resident","residente")]
    name = models.CharField(max_length=16, choices=GROUPS)
    
class CustomUser(AbstractUser,TimeStampedBy): # hereda de AbstractUser y TimeStampedBy
    ci = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=24, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    def __str__(self) -> str:  # útil en admin
        return f"{self.username} ({self.ci})"

