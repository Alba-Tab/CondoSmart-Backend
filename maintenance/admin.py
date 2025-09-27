from django.contrib import admin
from .models import Servicio, TicketMantenimiento, TarifaServicio

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_by", "updated_by", "created_at")
    search_fields = ("name", "descripcion")
    list_filter = ("is_active", "created_by", "updated_by")
    ordering = ("name",)

@admin.register(TicketMantenimiento)
class TicketMantenimientoAdmin(admin.ModelAdmin):
    list_display = (
        "id", "titulo", "unidad", "servicio", "estado",
        "programado", "cerrado", "created_by", "updated_by"
    )
    list_filter = ("estado", "servicio", "unidad", "created_by")
    search_fields = ("titulo", "descripcion", "unidad__code", "servicio__name")
    ordering = ("-programado",)

@admin.register(TarifaServicio)
class TarifaServicioAdmin(admin.ModelAdmin):
    list_display = (
        "id", "servicio", "monto", "vigente_desde",
        "vigente_hasta", "created_by", "updated_by"
    )
    list_filter = ("servicio", "vigente_desde", "vigente_hasta", "created_by")
    search_fields = ("servicio__name",)
    ordering = ("-vigente_desde",)