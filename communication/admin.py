from django.contrib import admin
from .models import Comunicado, Notificacion

@admin.register(Comunicado)
class ComunicadoAdmin(admin.ModelAdmin):
    list_display = ("pk", "titulo", "publicado_at", "created_by", "updated_by")
    search_fields = ("titulo", "cuerpo")
    list_filter = ("publicado_at", "created_by", "updated_by")

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "user", "tipo", "titulo", "publicado_at",
        "leido_at", "created_by", "updated_by"
    )
    search_fields = ("titulo", "cuerpo", "user__username", "user__ci")
    list_filter = ("tipo", "leido_at", "created_by", "updated_by")