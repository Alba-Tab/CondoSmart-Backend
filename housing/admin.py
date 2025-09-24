from django.contrib import admin

from django.contrib import admin
from .models import Unidad, Residency, Vehiculo, Mascota, Contrato

admin.site.register(Unidad)
admin.site.register(Residency)
admin.site.register(Vehiculo)
admin.site.register(Mascota)
admin.site.register(Contrato)