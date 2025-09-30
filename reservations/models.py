from django.db import models
from core.models import TimeStampedBy
from decimal import Decimal
from finance.models import Cargo


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
        
    def cancelar(self):
        if self.status != "pendiente":
            raise ValueError("Solo reservas pendientes pueden cancelarse.")
        Cargo.objects.filter(reserva=self, concepto="deposito", estado="pendiente").update(estado="anulado", saldo=Decimal("0.00"))
        self.status = "cancelada"
        self.save()
        
    def finalizar(self):
        if self.status != "confirmada":
            raise ValueError("Solo reservas confirmadas pueden finalizarse.")
        self.status = "finalizada"
        self.save()
        
    def __str__(self) -> str:
        return f"R{self.pk}-U{self.unidad.code} {self.start:%Y-%m-%d %H:%M} a {self.end:%Y-%m-%d %H:%M} [{self.status}]"
