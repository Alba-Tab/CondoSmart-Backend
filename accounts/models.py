from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedBy

class CustomUser(AbstractUser,TimeStampedBy): # hereda de AbstractUser y TimeStampedBy
    document_id = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=24, blank=True)

    def __str__(self) -> str:  # útil en admin
        return f"{self.username} ({self.document_id})"

class Rol(TimeStampedBy): # ya hereda models.Model de TimeStampedBy
    GROUPS = [("admin","administrador"),("guard","guardia"),("resident","residente")]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="roles")
    group_name = models.CharField(max_length=16, choices=GROUPS)
  # condo = models.ForeignKey("housing.Condo", null=True, blank=True, on_delete=models.CASCADE)
    unidad = models.ForeignKey("housing.Unidad", null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = [("user","group_name","unidad")]

    def __str__(self) -> str:
        scope = f"unidad:{self.unidad.id}" if self.unidad is not None else "global"
        return f"{self.user.username}:{self.group_name}@{scope}"