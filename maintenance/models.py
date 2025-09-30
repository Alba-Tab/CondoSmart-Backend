from django.db import models
from core.models import TimeStampedBy
from decimal import Decimal
from django.utils import timezone

class Servicio(TimeStampedBy):
    name = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        indexes = [models.Index(fields=["is_active","name"])]
    def __str__(self) -> str:
        estado = "" if self.is_active else "(inactivo)"
        return f"{self.name} {estado}"

class TicketMantenimiento(TimeStampedBy):
    ESTADO = [("abierto","abierto"),("en_progreso","en_progreso"),("resuelto","resuelto"),("cerrado","cerrado")]

    unidad = models.ForeignKey("housing.Unidad", on_delete=models.CASCADE, related_name="tickets_mant")
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="tickets")
    
    titulo = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=16, choices=ESTADO, default="abierto")
    programado = models.DateTimeField(null=True, blank=True) 
    cerrado = models.DateTimeField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    class Meta:
        indexes = [
            models.Index(fields=["unidad","estado"]),
            models.Index(fields=["programado"]),
            models.Index(fields=["cerrado"]),
        ]
        
    def generar_cargo(self, monto: Decimal, user):
        from finance.models import Cargo
        cargo = Cargo.objects.create(
            unidad=self.unidad,
            origen=self,  
            concepto="otro", 
            monto=monto,
            saldo=monto,
            created_by=user
        )

        # 2. Actualiza el precio del ticket con el monto del cargo
        self.precio = monto
        self.estado = 'resuelto'      # Marca el ticket como resuelto
        self.cerrado = timezone.now() # Establece la fecha de cierre
        self.updated_by = user
        self.save()

        return cargo
    def cancelar_ticket(self, user):
        if self.estado == "resuelto":
            raise ValueError("No se puede cancelar un ticket cerrado.")
        self.estado = "cerrado"
        self.cerrado = timezone.now()
        self.updated_by = user
        self.save()
