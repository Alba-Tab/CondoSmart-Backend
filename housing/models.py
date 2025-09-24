from django.db import models
from core.models import TimeStampedBy

class Unidad(TimeStampedBy):
    code = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.PROTECT, related_name="duenno", null=True, blank=True)

    def __str__(self):
        owner = self.user or "sin dueño"
        estado = "active" if self.is_active else "inactive"
        return f"{self.code} Dueño: {owner} ({estado})"
    
class Residency(TimeStampedBy):
    STATUS = [("activa","activa"),("inactiva","inactiva")]
    TIPO = [("propietario","propietario"),("inquilino","inquilino")]
    
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="residencias")
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name="residentes")
    is_owner = models.BooleanField(default=False)
    tipo_ocupacion = models.CharField(max_length=16, choices=TIPO, default="propietario")
    status = models.CharField(max_length=16, choices=STATUS, default="activa")
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    class Meta:
        indexes = [models.Index(fields=["unidad","user","status"])]
        unique_together = [("user","unidad","start")] 
    def __str__(self): 
        return f"{self.user.id}@{self.unidad.pk}"
    

class Vehiculo(TimeStampedBy):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    responsable = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="vehiculos", null=True, blank=True)
    placa = models.CharField(max_length=16, unique=True)
    marca = models.CharField(max_length=64, blank=True)
    color = models.CharField(max_length=32, blank=True)
    observacion = models.TextField(blank=True)
    def __str__(self): 
        return f"{self.placa} ({self.marca} {self.color})"
    
class Mascota(TimeStampedBy):
    TIPO = [("perro","perro"),("gato","gato"),("pez","pez"),("hamster","hamster"),("otro","otro")]
    nombre = models.CharField(max_length=120)
    raza = models.CharField(max_length=120, blank=True)
    tipo = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    desde = models.DateField(null=True, blank=True)
    hasta = models.DateField(null=True, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, related_name="mascotas", null=True, blank=True)
    responsable = models.ForeignKey("accounts.CustomUser", on_delete=models.SET_NULL, related_name="mascotas", null=True, blank=True)
    def __str__(self): 
        return f"{self.nombre} ({self.tipo} {self.raza})"
    
class Contrato (TimeStampedBy):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name="contratos")
    duenno = models.ForeignKey("accounts.CustomUser", on_delete=models.PROTECT, related_name="contratos", null=True, blank=True)
    inquilino = models.ForeignKey("accounts.CustomUser", on_delete=models.PROTECT, related_name="contratos_inquilino", null=True, blank=True)
    descripcion = models.TextField(blank=True)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    documento = models.FileField(upload_to="contratos/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    monto_mensual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        indexes = [models.Index(fields=["unidad","inquilino","is_active"])]
    def __str__(self): return f"C-{self.pk}@{self.unidad.pk}"