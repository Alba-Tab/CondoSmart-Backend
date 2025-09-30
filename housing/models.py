from django.db import models
from core.models import TimeStampedBy
from decimal import Decimal
class Condominio(TimeStampedBy):
    DIRECCION_TIPO = [("vertical","departamento"), ("horizontal","casa")]

    direccion = models.CharField(max_length=200)
    name = models.CharField(max_length=120)
    tipo = models.CharField(max_length=20, choices=DIRECCION_TIPO)

    def __str__(self):
        estado = "" if self.is_active else "(inactivo)"
        return f"{self.name} - {self.direccion} {estado}"

class Unidad(TimeStampedBy):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, related_name="unidades")
    direccion = models.CharField(max_length=200)
    code = models.CharField(max_length=32)
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.PROTECT, 
                             related_name="duenno", null=True, blank=True)
    piso = models.IntegerField(null=True, blank=True)  # Solo para departamentos
    manzano = models.CharField(max_length=10, blank=True, null=True)  # Solo para casas
    @property
    def tipo(self):
        return self.condominio.tipo  # Se hereda del condominio

    def __str__(self):
        estado = "" if self.is_active else "(inactivo)"
        if self.tipo == "departamento":
            return f"Piso {self.piso} - Depto {self.code} ({estado})"
        else:
            return f"Manzano {self.manzano} - Casa {self.code} ({estado})"
    
class Residency(TimeStampedBy):
    STATUS = [("activa","activa"),("inactiva","inactiva")]
    TIPO = [("propietario","propietario"),("inquilino","inquilino")]
    
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="residencias")
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name="residentes")
    tipo_ocupacion = models.CharField(max_length=16, choices=TIPO, default="propietario")
    status = models.CharField(max_length=16, choices=STATUS, default="activa")
    is_owner = models.BooleanField(default=False)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    
    class Meta:
        indexes = [models.Index(fields=["unidad","user","status"])]
        unique_together = [("user","unidad")] 
    def __str__(self): 
        estado = "" if self.is_active else "(inactivo)"
        return f"U{self.unidad.code}-R{self.user.username} ({self.tipo_ocupacion}) {estado}"
    

class Vehiculo(TimeStampedBy):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    responsable = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="vehiculos", null=True, blank=True)
    placa = models.CharField(max_length=16, unique=True)
    marca = models.CharField(max_length=64, blank=True)
    color = models.CharField(max_length=32, blank=True)
    observacion = models.TextField(blank=True)
    def __str__(self): 
        if self.responsable:
            return f"{self.placa} ({self.marca} {self.color}) Dueño : {self.responsable.first_name}"
        return f"{self.placa} ({self.marca} {self.color}) Externo"
    
class Mascota(TimeStampedBy):
    TIPO = [("perro","perro"),("gato","gato"),("pez","pez"),("hamster","hamster"),("otro","otro")]
    name = models.CharField(max_length=120)
    raza = models.CharField(max_length=120, blank=True)
    tipo = models.CharField(max_length=120, blank=True)
    desde = models.DateField(null=True, blank=True)
    hasta = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="mascotas", null=True, blank=True)
    def __str__(self): 
        if self.responsable:
            return f"{self.name} ({self.tipo} {self.raza}) Dueño : {self.responsable.first_name}"
        return f"{self.name} ({self.tipo} {self.raza}) Dueño : Sin responsable" 
    
class Contrato (TimeStampedBy):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name="contratos")
    duenno = models.ForeignKey("accounts.CustomUser", on_delete=models.PROTECT, related_name="contratos", null=True, blank=True)
    inquilino = models.ForeignKey("accounts.CustomUser", on_delete=models.PROTECT, related_name="contratos_inquilino", null=True, blank=True)
    descripcion = models.TextField(blank=True)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    documento = models.FileField(upload_to="contratos/", null=True, blank=True)
    monto_mensual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        indexes = [models.Index(fields=["unidad","inquilino"])]
    def __str__(self): 
        estado = "" if self.is_active else "(inactivo)"
        return f"U{self.unidad.code}-C{self.pk} D:{self.duenno} I:{self.inquilino} {estado}"

    def generar_cargo_mensual(self, periodo, monto=None):
        from finance.models import Cargo
        monto = monto or self.monto_mensual or Decimal("0.00")

        # evitar duplicados
        if Cargo.objects.filter(origen=self, periodo=periodo).exists():
            return None  

        cargo = Cargo.objects.create(
            unidad=self.unidad,
            origen=self,
            concepto="cuota",
            descripcion=f"Expensa mensual {periodo:%Y-%m} (Contrato {self.pk})",
            monto=monto,
            saldo=monto,
            periodo=periodo,
        )
        return cargo