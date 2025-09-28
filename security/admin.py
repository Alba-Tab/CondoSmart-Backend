from django.contrib import admin
from .models import Visita, Acceso, AccesoEvidencia, Incidente


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "documento", "telefono", "user", "created_by", "created_at")
    search_fields = ("nombre", "documento", "telefono", "user__username")
    list_filter = ("created_by", "created_at")
    ordering = ("-created_at",)


@admin.register(Acceso)
class AccesoAdmin(admin.ModelAdmin):
    list_display = ("id", "unidad", "sentido", "permitido", "created_by", "created_at")
    search_fields = ("unidad__code",)
    list_filter = ("sentido", "permitido", "unidad", "created_by")
    ordering = ("-created_at",)


@admin.register(AccesoEvidencia)
class AccesoEvidenciaAdmin(admin.ModelAdmin):
    list_display = (
        "id", "acceso", "tipo", "modo", "user", "visita",
        "vehiculo", "match", "evidencia_s3", "created_by", "created_at"
    )
    search_fields = (
        "user__username", "visita__nombre", "vehiculo__placa",
        "acceso__unidad__code"
    )
    list_filter = ("tipo", "modo", "match", "created_by", "created_at")
    ordering = ("-created_at",)


@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ("id", "unidad", "user", "titulo", "estado", "created_by", "created_at")
    search_fields = ("titulo", "descripcion", "unidad__code", "user__username")
    list_filter = ("estado", "unidad", "created_by")
    ordering = ("-created_at",)
