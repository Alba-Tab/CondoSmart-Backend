from rest_framework import serializers
from .models import Cargo, Pago, PagoCargo

class CargoSerializer(serializers.ModelSerializer):
    class Meta: model = Cargo; fields = "__all__"

class PagoSerializer(serializers.ModelSerializer):
    class Meta: model = Pago; fields = "__all__"

class PagoCargoSerializer(serializers.ModelSerializer):
    class Meta: model = PagoCargo; fields = "__all__"