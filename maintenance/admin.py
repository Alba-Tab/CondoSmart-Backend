from django.contrib import admin
from .models import Servicio, TicketMantenimiento, TarifaServicio

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("id","name","is_active","created_at")
    search_fields = ("name",)

@admin.register(TicketMantenimiento)
class TicketMantenimientoAdmin(admin.ModelAdmin):
    list_display = ("id","titulo","unidad","servicio","estado","programado","cerrado")
    list_filter = ("estado", "servicio")
    search_fields = ("titulo","descripcion")

@admin.register(TarifaServicio)
class TarifaServicioAdmin(admin.ModelAdmin):
    list_display = ("id","servicio","monto","vigente_desde","vigente_hasta","created_at")
    list_filter = ("servicio",)
    search_fields = ("servicio__name",)