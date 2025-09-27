from django.contrib import admin
from .models import AreaComun, Suministro, Reserva, ReservaSuministro

@admin.register(AreaComun)
class AreaComunAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "requires_deposit", "deposit_amount", "is_active", "created_by", "updated_by")
    search_fields = ("name", "descripcion")
    list_filter = ("requires_deposit", "is_active", "created_by")
    ordering = ("name",)

@admin.register(Suministro)
class SuministroAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "cantidad_total", "restante")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("id", "unidad", "area", "start", "end", "status", "created_by")
    search_fields = ("unidad__code", "area__name", "notas")
    list_filter = ("status", "area", "start", "end", "created_by")
    ordering = ("-start",)

@admin.register(ReservaSuministro)
class ReservaSuministroAdmin(admin.ModelAdmin):
    list_display = ("id", "reserva", "suministro", "cantidad")
    search_fields = ("reserva__unidad__code", "suministro__nombre")
    list_filter = ("suministro",)
    ordering = ("reserva",)
