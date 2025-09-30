from django.db import models
from core.models import TimeStampedBy
from decimal import Decimal
from finance.models import Cargo
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class AreaComun(TimeStampedBy):
    name = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    
    class Meta:
        indexes = [models.Index(fields=["name"])]
    def __str__(self) -> str:
        return self.name

class Suministro(TimeStampedBy):
    name = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    cantidad_total = models.PositiveIntegerField(default=1)
    areacomun = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name="suministros")
    def __str__(self):
        return self.name


class Reserva(TimeStampedBy):

    STATUS = [("pendiente","pendiente"),("confirmada","confirmada"),
              ("finalizada", "finalizada"),("cancelada","cancelada")]

    unidad = models.ForeignKey("housing.Unidad", on_delete=models.CASCADE, related_name="reservas")
    area = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name="reservas", null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=16, choices=STATUS, default="pendiente")
    notas = models.TextField(blank=True)
    class Meta:
        indexes = [
            models.Index(fields=["unidad","area","start","end"]),
            models.Index(fields=["status"]),
        ] 
    
    def create_cargo_if_required(self):
        if self.area and self.area.deposit_amount > 0:
            Cargo.objects.create(
                unidad=self.unidad,
                origen=self,
                concepto="deposito",
                monto=self.area.deposit_amount,
                descripcion=f"Depósito reserva área {self.area.name}",
                saldo=self.area.deposit_amount,
            )
    # metodo llamado por cargo para confirmar la reserva
    def confirmar(self):
        if self.status != "pendiente" and self.area and self.area.deposit_amount > 0:
            raise ValueError("Solo reservas pendientes y sin depósito pueden confirmarse.")
        self.status = "confirmada"
        self.save()
        
    def cancelar(self,user):
        if self.status == 'cancelada':
            raise ValueError("La reserva ya está cancelada.")
        if self.status != "pendiente":
            raise ValueError("Solo reservas pendientes pueden cancelarse.")
        content_type = ContentType.objects.get_for_model(self)
        cargo_deposito = Cargo.objects.filter(
            content_type=content_type,
            object_id=self.pk,
            concepto="deposito"
        ).first()
        if cargo_deposito and cargo_deposito.estado != 'anulado':
            cargo_deposito.anular()
            # Asigna el usuario que realizó la anulación
            cargo_deposito.updated_by = user
            cargo_deposito.save()

        self.status = 'cancelada'
        self.updated_by = user
        self.save()
        
    def finalizar(self):
        if self.status != "confirmada":
            raise ValueError("Solo reservas confirmadas pueden finalizarse.")
        self.status = "finalizada"
        self.save()
        
    def __str__(self) -> str:
        return f"R{self.pk}-U{self.unidad.code} {self.start:%Y-%m-%d %H:%M} a {self.end:%Y-%m-%d %H:%M} [{self.status}]"
