from rest_framework import serializers
from .models import Unidad, Residency

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = '__all__'

class ResidencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Residency
        fields = '__all__'