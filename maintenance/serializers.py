from rest_framework import serializers
from .models import Servicio, TicketMantenimiento, TarifaServicio

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"

class TicketMantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMantenimiento
        fields = "__all__"

class TarifaServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaServicio
        fields = "__all__"
