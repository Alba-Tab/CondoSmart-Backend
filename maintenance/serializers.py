from rest_framework import serializers
from .models import Servicio, TicketMantenimiento

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"

class TicketMantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMantenimiento
        fields = "__all__"

