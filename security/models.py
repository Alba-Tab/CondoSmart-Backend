from django.db import models
from core.models import TimeStampedBy
from django.utils.timezone import now, timedelta
from decimal import Decimal
from finance.models import Cargo
class Visita(TimeStampedBy):
    name = models.CharField(max_length=120)
    documento = models.CharField(max_length=32, unique=True)
    telefono = models.CharField(max_length=24, blank=True)
    photo_key = models.CharField(max_length=255, blank=True, null=True) 
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    dias_permiso = models.IntegerField(default=1)
    
    class Meta:
        indexes = [models.Index(fields=["documento"])]

    def __str__(self) -> str:
        return f"{self.name} ({self.documento})"
    
    def permitido(self):
        inicio = self.fecha_inicio or self.created_at
        fin = inicio + timedelta(days=self.dias_permiso)
        return inicio <= now() <= fin

class Acceso(TimeStampedBy):
    SENTIDOS = [("in","in"),("out","out")]
    
    unidad = models.ForeignKey("housing.Unidad", on_delete=models.CASCADE, related_name="accesos")
    sentido = models.CharField(max_length=16, choices=SENTIDOS, default="in")
    permitido = models.BooleanField(default=False)
    
    class Meta:
        indexes = [models.Index(fields=["unidad","created_at"])]
    def __str__(self) -> str:
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.sentido}  @U{self.unidad.code}"

class AccesoEvidencia(TimeStampedBy):
    MODO = [("manual", "manual"), ("face", "face"), ("placa", "placa")]
    TIPOS = [("usuario","usuario"), ("externo","externo"), ("vehiculo","vehiculo")]

    acceso = models.ForeignKey(Acceso, on_delete=models.CASCADE, related_name="evidencias")
    modo = models.CharField(max_length=16, choices=MODO)
    tipo = models.CharField(max_length=16, choices=TIPOS, default="usuario")
    
    user = models.ForeignKey("accounts.CustomUser", null=True, blank=True, on_delete=models.SET_NULL)
    visita = models.ForeignKey("Visita", null=True, blank=True, on_delete=models.SET_NULL)
    vehiculo = models.ForeignKey("housing.Vehiculo", null=True, blank=True, on_delete=models.SET_NULL)

    match = models.BooleanField(default=False)
    evidencia_s3 = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"Evidencia {self.modo} - {self.tipo} ({'match' if self.match else 'no match'})"
    
    def validar(self):
        return self.visita and self.visita.is_activa()

class Incidente(TimeStampedBy):
    ESTADO = [("abierto","abierto"),("en_progreso","en_progreso"),("cerrado","cerrado")]
    
    unidad = models.ForeignKey("housing.Unidad", on_delete=models.CASCADE, related_name="incidentes")
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="incidentes")
    titulo = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=16, choices=ESTADO, default="abierto")
    evidencia_s3 = models.CharField(max_length=256, blank=True)
    class Meta:
        indexes = [models.Index(fields=["unidad","estado","created_at"])]
    def __str__(self) -> str:
        estado = "" if self.is_active else "(inactivo)"
        return f"I{self.titulo}:{self.estado}@U{self.unidad.code} {estado}"
    def generar_cargo(self, monto: Decimal, descripcion: str = ""):
          
        descripcion = descripcion if descripcion != "" else f"Multa por incidente {self.pk} - {self.titulo}"
        cargo = Cargo.objects.create(
            unidad=self.unidad,
            origen=self,  
            concepto="multa",
            monto=monto,
            saldo=monto,
            descripcion=descripcion,
        )
        return cargo