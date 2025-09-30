from django.contrib import admin
from .models import AreaComun, Suministro, Reserva

@admin.register(AreaComun)
class AreaComunAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'deposit_required']
    # No se puede filtrar por un método, usa el campo real o quítalo.
    # Lo quitaremos para simplificar.
    list_filter = ('is_active',) 
    search_fields = ("name", "descripcion")
    ordering = ("name",)

    @admin.display(boolean=True, description='Requiere Depósito?')
    def deposit_required(self, obj):
        return obj.deposit_amount > 0

@admin.register(Suministro)
class SuministroAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cantidad_total']
    search_fields = ("name", "descripcion")
    ordering = ("name",)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("id", "unidad", "area", "start", "end", "status", "created_by")
    search_fields = ("unidad__code", "area__name", "notas")
    list_filter = ("status", "area", "start", "end", "created_by")
    ordering = ("-start",)
