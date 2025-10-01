from django.contrib import admin
from .models import Unidad, Residency, Vehiculo, Mascota, Contrato, Condominio
@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "direccion", "created_by", "updated_by")
    search_fields = ("name", "direccion")
    ordering = ("name",)

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "is_active", "user", "created_by", "updated_by")
    search_fields = ("code", "user__username", "user__first_name", "user__last_name")
    list_filter = ("is_active", "created_by", "updated_by")
    ordering = ("code",)

@admin.register(Residency)
class ResidencyAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "unidad", "tipo_ocupacion", "status", "start", "end", "created_by")
    search_fields = ("user__username", "unidad__code")
    list_filter = ("tipo_ocupacion", "status", "start", "end", "created_by")
    ordering = ("-start",)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("id", "placa", "unidad", "responsable", "marca", "color", "created_by")
    search_fields = ("placa", "marca", "color", "responsable__username")
    list_filter = ("marca", "color", "created_by")
    ordering = ("placa",)

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tipo", "raza", "responsable", "is_active", "created_by")
    search_fields = ("name", "raza", "responsable__username")
    list_filter = ("tipo", "is_active", "created_by")
    ordering = ("name",)

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ("id", "unidad", "duenno", "inquilino", "is_active", "start", "end", "monto_mensual", "created_by")
    search_fields = ("unidad__code", "duenno__username", "inquilino__username")
    list_filter = ("is_active", "start", "end", "created_by")
    ordering = ("-start",)