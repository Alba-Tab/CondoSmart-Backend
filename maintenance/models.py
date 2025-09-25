from django.db import models
from core.models import TimeStampedBy

class Servicio(TimeStampedBy):
    name = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        indexes = [models.Index(fields=["is_active","name"])]
    def __str__(self) -> str:
        return self.name

class TicketMantenimiento(TimeStampedBy):
    ESTADO = [("abierto","abierto"),("en_progreso","en_progreso"),("resuelto","resuelto"),("cerrado","cerrado")]

    unidad = models.ForeignKey("housing.Unidad", on_delete=models.CASCADE, related_name="tickets_mant")
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, related_name="tickets")
    titulo = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=16, choices=ESTADO, default="abierto")
    programado = models.DateTimeField(null=True, blank=True) 
    cerrado = models.DateTimeField(null=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=["unidad","estado"]),
            models.Index(fields=["programado"]),
            models.Index(fields=["cerrado"]),
        ]
    def __str__(self) -> str:
        return f"T{self.pk}:{self.titulo[:20]}"
class TarifaServicio(TimeStampedBy):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="tarifas")
    descripcion = models.CharField(max_length=160, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField(null=True, blank=True)
    class Meta:
        indexes = [models.Index(fields=["servicio","vigente_desde","vigente_hasta"])]
        unique_together = [("servicio","vigente_desde")]
    def __str__(self) -> str:
        return f"{self.servicio.name} ${self.monto} desde {self.vigente_desde}"
