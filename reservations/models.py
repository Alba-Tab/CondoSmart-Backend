from django.db import models
from core.models import TimeStampedBy
from decimal import Decimal

class AreaComun(TimeStampedBy):
    name = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    requires_deposit = models.BooleanField(default=False)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [models.Index(fields=["is_active","name"])]
    def __str__(self) -> str:
        return self.name

class Suministro(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    cantidad_total = models.PositiveIntegerField(default=1)
    # area = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name="suministros", null=True, blank=True)  # Opcional

    def __str__(self):
        return self.nombre

class ReservaSuministro(models.Model):
    reserva = models.ForeignKey("Reserva", on_delete=models.CASCADE, related_name="reservasuministros")
    suministro = models.ForeignKey(Suministro, on_delete=models.CASCADE, related_name="reservasuministros")
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = [("reserva", "suministro")]

class Reserva(TimeStampedBy):
    STATUS = [("pendiente","pendiente"),("confirmada","confirmada"),("cancelada","cancelada")]
    unidad = models.ForeignKey("housing.Unidad", on_delete=models.CASCADE, related_name="reservas")
    area = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name="reservas")
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=16, choices=STATUS, default="pendiente")
    notas = models.TextField(blank=True)
    class Meta:
        indexes = [
            models.Index(fields=["unidad","area","start","end"]),
            models.Index(fields=["status"]),
        ]
    def __str__(self) -> str:
        return f"R{self.pk}@U{self.unidad.id}:{self.area.pk}"