from django.db import models
from core.models import TimeStampedBy
from decimal import Decimal
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Cargo(TimeStampedBy):
    TIPO = [("cuota","cuota"),("multa","multa"),("deposito","deposito"),("otro","otro")]
    ESTADO = [("pendiente","pendiente"),("parcial","parcial"),("pagado","pagado"),("anulado","anulado")]

    unidad = models.ForeignKey("housing.Unidad", on_delete=models.CASCADE, related_name="cargos")
    
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    origen = GenericForeignKey("content_type", "object_id")
    
    concepto = models.CharField(max_length=16, choices=TIPO, default="cuota")
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=16, choices=ESTADO, default="pendiente")
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) 
    periodo = models.DateField(null=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=["unidad","concepto","estado","periodo"]),
        ]
    def registrar_pago(self, monto_pago: Decimal):
        if self.estado in ["pagado", "anulado"]:
            raise ValueError("No se puede pagar un cargo ya cerrado.")

        nuevo_saldo = self.saldo - monto_pago
        if nuevo_saldo <= 0:
            self.saldo = Decimal("0.00")
            self.estado = "pagado"
        else:
            self.saldo = nuevo_saldo
            self.estado = "parcial"
        self.save()

    def anular(self):
        self.estado = "anulado"
        self.saldo = Decimal("0.00")
        self.save()
        
    def __str__(self):
        return f"{self.concepto} ${self.monto} U{self.unidad.id} [{self.estado}]"

    
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
    def __str__(self): 
        estado = "" if self.is_active else "(inactivo)"
        return f"P{self.pk}-U{self.user.id} ${self.monto_total} {estado}"
    
    def confirmar(self):
        if self.estado != "pendiente":
            raise ValueError("Solo pagos pendientes pueden confirmarse.")
        pagos = PagoCargo.objects.filter(pago=self)
        for pc in pagos:
            cargo = pc.cargo
            cargo.registrar_pago(pc.monto) 
        self.estado = "confirmado"
        self.save()

    def marcar_fallido(self):
        if self.estado == "pendiente":
            self.estado = "fallido"
            self.save()
            
class PagoCargo(TimeStampedBy):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name="aplicaciones")
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name="pagos")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        indexes = [models.Index(fields=["pago","cargo"])]
    def __str__(self): 
        estado = "" if self.is_active else "(inactivo)"
        return f"P{self.pago.pk}-C{self.cargo.pk} ${self.monto} {estado}"

    