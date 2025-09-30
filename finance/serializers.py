from rest_framework import serializers
from core.services import upload_fileobj, get_presigned_url
from .models import Pago, Cargo, PagoCargo

class CargoSerializer(serializers.ModelSerializer):
    origen_type = serializers.CharField(source="content_type.model", read_only=True)
    origen_id = serializers.IntegerField(source="object_id", read_only=True)

    class Meta:
        model = Cargo
        fields = "__all__"

class PagoSerializer(serializers.ModelSerializer):
    comprobante = serializers.FileField(write_only=True, required=False) 
    comprobante_url = serializers.SerializerMethodField()

    class Meta:
        model = Pago
        fields = [
            "id", "user", "fecha", "monto_total", "estado", "metodo","is_active",
            "observacion", "comprobante_key", "comprobante", "comprobante_url"
        ]
        read_only_fields = ["comprobante_key"]

    def create(self, validated_data):
        comprobante = validated_data.pop("comprobante", None)
        pago = super().create(validated_data)

        if comprobante:
            key = f"pagos/{pago.user_id}/pago_{pago.id}.jpg"
            upload_fileobj(comprobante, key)  # directo sin pasar por disco
            pago.comprobante_key = key
            pago.save()

        return pago

    def update(self, instance, validated_data):
        comprobante = validated_data.pop("comprobante", None)

        # Actualiza los demás campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if comprobante:
            key = f"pagos/{instance.user_id}/pago_{instance.id}.jpg"
            upload_fileobj(comprobante, key)
            instance.comprobante_key = key

        instance.save()
        return instance
    def get_comprobante_url(self, obj):
        if obj.comprobante_key:
            return get_presigned_url(obj.comprobante_key, expires_in=300)
        return None

class PagoCargoSerializer(serializers.ModelSerializer):
    class Meta: model = PagoCargo; fields = "__all__"