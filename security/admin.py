from django.contrib import admin
from .models import Visita, Acceso, Incidente

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "documento", "telefono", "user", "created_by", "created_at")
    search_fields = ("nombre", "documento", "telefono", "user__username")
    list_filter = ("created_by", "created_at")
    ordering = ("-created_at",)

@admin.register(Acceso)
class AccesoAdmin(admin.ModelAdmin):
    list_display = ("id", "unidad", "tipo", "modo", "sentido", "visita", "user", "vehiculo", "fecha", "created_by")
    search_fields = (
        "visita__nombre", "visita__documento",
        "user__username", "vehiculo__placa", "unidad__code"
    )
    list_filter = ("tipo", "modo", "sentido", "fecha", "unidad")
    ordering = ("-fecha",)

@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ("id", "unidad", "user", "titulo", "estado", "created_by", "created_at")
    search_fields = ("titulo", "descripcion", "unidad__code", "user__username")
    list_filter = ("estado", "unidad", "created_by")
    ordering = ("-created_at",)
