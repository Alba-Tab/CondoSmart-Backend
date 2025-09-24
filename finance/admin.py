from django.contrib import admin
from .models import Cargo, Pago, PagoCargo
admin.site.register(Cargo)
admin.site.register(Pago)
admin.site.register(PagoCargo)
