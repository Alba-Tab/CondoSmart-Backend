from django.db import models
from core.models import TimeStampedBy
from decimal import Decimal

class Cargo(TimeStampedBy):
    TIPO = [("cuota","cuota"),("multa","multa"),("deposito","deposito"),("otro","otro")]
    ESTADO = [("pendiente","pendiente"),("parcial","parcial"),("pagado","pagado"),("anulado","anulado")]

    unidad = models.ForeignKey("housing.Unidad", on_delete=models.CASCADE, related_name="cargos")
    reserva = models.ForeignKey("reservations.Reserva", on_delete=models.CASCADE, related_name="cargos", null=True, blank=True)
    concepto = models.CharField(max_length=16, choices=TIPO, default="cuota")
    descripcion = models.CharField(max_length=200, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    periodo = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=16, choices=ESTADO, default="pendiente")
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) # Saldo pendiente
    def __str__(self): return f"{self.concepto} ${self.monto} U{self.unidad.id}"
    
class Pago(TimeStampedBy):
    ESTADO = [("pendiente","pendiente"),("confirmado","confirmado"),("fallido","fallido")]
    METODO = [("efectivo","efectivo"),("tarjeta","tarjeta"),("transferencia","transferencia"),("otro","otro")]
    
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="user")
    fecha = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=16, choices=ESTADO, default="pendiente")
    metodo = models.CharField(max_length=64, choices=METODO, default="efectivo")
    comprobante_key = models.CharField(max_length=128, blank=True, null=True) 
    observacion = models.TextField(blank=True)
    def __str__(self): return f"P{self.pk} U{self.user.id} ${self.monto_total}"
    
class PagoCargo(TimeStampedBy):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name="aplicaciones")
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name="pagos")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    orden = models.PositiveIntegerField(default=1)
    class Meta:
        indexes = [models.Index(fields=["pago","cargo"])]
    def __str__(self): return f"P{self.pago.pk}-C{self.cargo.pk} ${self.monto}"
    

    