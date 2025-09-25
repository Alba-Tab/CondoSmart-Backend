from django.contrib import admin
from .models import AreaComun, Reserva, ReservaSuministro, Suministro
admin.site.register(AreaComun)
admin.site.register(Suministro)
admin.site.register(Reserva)
admin.site.register(ReservaSuministro)