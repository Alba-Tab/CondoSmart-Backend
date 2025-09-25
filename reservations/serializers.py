from rest_framework import serializers
from .models import AreaComun, Reserva, Suministro, ReservaSuministro

class AreaComunSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaComun
        fields = "__all__"

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"

class SuministroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suministro
        fields = "__all__"

class ReservaSuministroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaSuministro
        fields = "__all__"