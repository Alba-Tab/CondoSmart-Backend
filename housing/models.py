from django.db import models
from core.models import TimeStampedBy

#class Condo(TimeStampedBy):
#   name = models.CharField(max_length=120)

class Unidad(TimeStampedBy):
    #condo = models.ForeignKey(Condo, on_delete=models.CASCADE, related_name="unidades")
    code = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    # class Meta:
    #     unique_together = [("condo","code")]

class Residency(TimeStampedBy):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="residencias")
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name="residentes")
    is_owner = models.BooleanField(default=False)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

class Vehiculo(TimeStampedBy):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    placa = models.CharField(max_length=16, unique=True)
    marca = models.CharField(max_length=64, blank=True)
    color = models.CharField(max_length=32, blank=True)
    