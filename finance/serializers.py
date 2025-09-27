from rest_framework import serializers
from core.services import upload_file, get_presigned_url
import uuid, os
from .models import Pago, Cargo, PagoCargo

class CargoSerializer(serializers.ModelSerializer):
    class Meta: model = Cargo; fields = "__all__"

class PagoSerializer(serializers.ModelSerializer):
    comprobante = serializers.FileField(write_only=True, required=False) 
    comprobante_url = serializers.SerializerMethodField()

    class Meta:
        model = Pago
        fields = [
            "id", "user", "fecha", "monto_total", "estado", "metodo",
            "observacion", "comprobante_key", "comprobante", "comprobante_url"
        ]
        read_only_fields = ["comprobante_key"]

    def create(self, validated_data):
        comprobante = validated_data.pop("comprobante", None)
        pago = super().create(validated_data)

        if comprobante:
            tmp_path = f"/tmp/{uuid.uuid4()}_{comprobante.name}"
            with open(tmp_path, "wb+") as dest:
                for chunk in comprobante.chunks():
                    dest.write(chunk)

            # Guardamos en carpeta pagos con fecha y ID
            key = f"pagos/{pago.user_id}/{uuid.uuid4()}_{comprobante.name}"
            upload_file(tmp_path, key)
            os.remove(tmp_path)

            pago.comprobante_key = key
            pago.save()

        return pago

    def update(self, instance, validated_data):
        comprobante = validated_data.pop("comprobante", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if comprobante:
            tmp_path = f"/tmp/{uuid.uuid4()}_{comprobante.name}"
            with open(tmp_path, "wb+") as dest:
                for chunk in comprobante.chunks():
                    dest.write(chunk)

            key = f"pagos/{instance.user_id}/{uuid.uuid4()}_{comprobante.name}"
            upload_file(tmp_path, key)
            os.remove(tmp_path)

            instance.comprobante_key = key

        instance.save()
        return instance

    def get_comprobante_url(self, obj):
        if obj.comprobante_key:
            return get_presigned_url(obj.comprobante_key, expires_in=300)
        return None

class PagoCargoSerializer(serializers.ModelSerializer):
    class Meta: model = PagoCargo; fields = "__all__"