from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedBy

class CustomUser(AbstractUser,TimeStampedBy): # hereda de AbstractUser y TimeStampedBy
    id_document = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=24, blank=True)
    

class Rol(TimeStampedBy): # ya hereda models.Model de TimeStampedBy
    GROUPS = [("admin","administrador"),("guard","guardia"),("resident","residente")]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="roles")
    group_name = models.CharField(max_length=16, choices=GROUPS)
  # condo = models.ForeignKey("housing.Condo", null=True, blank=True, on_delete=models.CASCADE)
 # unidad = models.ForeignKey("housing.Unidad", null=True, blank=True, on_delete=models.CASCADE)