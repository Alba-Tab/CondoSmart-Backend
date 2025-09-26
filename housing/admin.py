from django.contrib import admin

from django.contrib import admin
from .models import Unidad, Residency, Vehiculo, Mascota, Contrato

admin.site.register(Residency)
admin.site.register(Vehiculo)
admin.site.register(Mascota)
admin.site.register(Contrato)

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ('id','code', 'is_active', 'user')
    list_filter = ('is_active', )
    search_fields = ('code', 'user__username', 'user__first_name', 'user__last_name')
