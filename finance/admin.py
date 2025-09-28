from django.contrib import admin
from .models import Cargo, Pago, PagoCargo
@admin.register(Cargo)

class CargoAdmin(admin.ModelAdmin):
    list_display = ("pk", "unidad", "concepto", "monto", "estado", "saldo", "periodo", "created_by")
    search_fields = ("descripcion", "unidad__id")
    list_filter = ("concepto", "estado", "periodo", "created_by", "updated_by")
    ordering = ("-periodo",)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "fecha", "monto_total", "estado", "metodo", "created_by")
    search_fields = ("user__username", "user__ci", "observacion")
    list_filter = ("estado", "metodo", "fecha", "created_by", "updated_by")
    ordering = ("-fecha",)

@admin.register(PagoCargo)
class PagoCargoAdmin(admin.ModelAdmin):
    list_display = ("pk", "pago", "cargo", "monto", "orden", "created_by")
    search_fields = ("pago__user__username", "cargo__descripcion")
    list_filter = ("created_by", "updated_by")
    ordering = ("pago", "orden")