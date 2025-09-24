from rest_framework import serializers
from .models import Visita, Acceso, Incidente

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = "__all__"

class AccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acceso
        fields = "__all__"

class IncidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidente
        fields = "__all__"