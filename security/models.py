from django.db import models
from core.models import TimeStampedBy

class Visita(TimeStampedBy):
    nombre = models.CharField(max_length=120)
    documento = models.CharField(max_length=32)
    telefono = models.CharField(max_length=24, blank=True)
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="visitas")
    photo_key = models.CharField(max_length=255, blank=True) 
    class Meta:
        indexes = [models.Index(fields=["documento"])]
    def __str__(self) -> str:
        return f"{self.nombre} ({self.documento}) visita de U{self.user.first_name}"

class Acceso(TimeStampedBy):
    METODOS = [("manual","manual"),("placas","placas"),("face","face")]
    SENTIDOS = [("in","in"),("out","out")]
    TIPOS = [("visita","visita"),("vehiculo","vehiculo"),("residente","residente")]
    
    unidad = models.ForeignKey("housing.Unidad", on_delete=models.CASCADE, related_name="accesos")
    visita = models.ForeignKey(Visita, null=True, blank=True, on_delete=models.SET_NULL, related_name="accesos")
    user = models.ForeignKey("accounts.CustomUser", null=True, blank=True, on_delete=models.SET_NULL, related_name="accesos")
    vehiculo = models.ForeignKey("housing.Vehiculo", null=True, blank=True, on_delete=models.SET_NULL, related_name="accesos")
    modo = models.CharField(max_length=16, choices=METODOS, default="manual")  
    sentido = models.CharField(max_length=16, choices=SENTIDOS, default="in")
    tipo = models.CharField(max_length=16, choices=TIPOS, default="visita")
    fecha = models.DateTimeField(auto_now_add=True) 
    evidencia_key = models.CharField(max_length=256, blank=True)  
    class Meta:
        indexes = [models.Index(fields=["unidad","fecha"])]
    def __str__(self) -> str:
        return f"{self.tipo}:{self.modo}@U{self.unidad.code} {self.fecha.isoformat()}"

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
        return f"I{self.titulo}:{self.estado}@U{self.unidad.code}"