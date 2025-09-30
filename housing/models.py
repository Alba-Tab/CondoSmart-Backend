from django.db import models
from core.models import TimeStampedBy

class Unidad(TimeStampedBy):
    code = models.CharField(max_length=32)
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.PROTECT, 
                             related_name="duenno", null=True, blank=True)

    def __str__(self):
        owner = self.user or "Condominio"
        estado = "" if self.is_active else "inactive"
        return f"{self.code} Dueño: {owner} ({estado})"
    
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