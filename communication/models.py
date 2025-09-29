from django.db import models
from core.models import TimeStampedBy

class Comunicado(TimeStampedBy):
    titulo = models.CharField(max_length=160)
    cuerpo = models.TextField()
    publicado_at = models.DateTimeField(null=True, blank=True)  
    
    class Meta:
        indexes = [models.Index(fields=["publicado_at"])]
    def __str__(self) -> str:
        return f"{self.titulo}"

class Notificacion(TimeStampedBy):
    TIPO = [("deuda","deuda"),("multa","multa"),("evento","evento"),("comunicado","comunicado"),("otro","otro")]
    
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="notificaciones")
    comunicado = models.ForeignKey(Comunicado, null=True, blank=True, on_delete=models.CASCADE, related_name="notificaciones")
    tipo = models.CharField(max_length=32, blank=True, choices=TIPO) 
    referencia_id = models.PositiveIntegerField(null=True, blank=True)  # para enlazar con otros modelos
    titulo = models.CharField(max_length=160)
    cuerpo = models.TextField(blank=True)
    publicado_at = models.DateTimeField(null=True, blank=True) 
    leido_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [models.Index(fields=["user","leido_at"])]
    def __str__(self) -> str:
        return f"notif:{self.user.username}:{self.titulo[:20]}"