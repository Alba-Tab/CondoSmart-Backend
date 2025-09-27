from rest_framework import serializers
from core.services import upload_file, get_presigned_url
from .models import Visita, Acceso, Incidente
from core.services import get_presigned_url
import uuid, os

class VisitaSerializer(serializers.ModelSerializer):
    # Campo solo para recibir archivo en POST
    foto = serializers.ImageField(write_only=True, required=False)
    # Campo solo de salida
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Visita
        fields = ["id", "nombre", "documento", "telefono", "user", "photo_key", "foto", "foto_url"]
        read_only_fields = ["photo_key"]

    def create(self, validated_data):
        foto = validated_data.pop("foto", None)
        visita = super().create(validated_data)

        if foto:
            tmp_path = f"/tmp/{uuid.uuid4()}.jpg"
            with open(tmp_path, "wb+") as dest:
                for chunk in foto.chunks():
                    dest.write(chunk)

            key = f"visitas/{visita.id}/foto.jpg"
            upload_file(tmp_path, key)
            os.remove(tmp_path)

            visita.photo_key = key
            visita.save()

        return visita

    def get_foto_url(self, obj):
        if obj.photo_key:
            return get_presigned_url(obj.photo_key, expires_in=300)
        return None

class AccesoSerializer(serializers.ModelSerializer):
    evidencia = serializers.ImageField(write_only=True, required=False)
    evidencia_url = serializers.SerializerMethodField()

    class Meta:
        model = Acceso
        fields = [
            "id", "unidad", "visita", "user", "vehiculo",
            "modo", "sentido", "tipo", "fecha",
            "match", "permitido",
            "evidencia_s3", "evidencia", "evidencia_url"
        ]
        read_only_fields = ["evidencia_s3", "fecha"]

    def create(self, validated_data):
        evidencia = validated_data.pop("evidencia", None)
        acceso = super().create(validated_data)

        if evidencia:
            tmp_path = f"/tmp/{uuid.uuid4()}.jpg"
            with open(tmp_path, "wb+") as dest:
                for chunk in evidencia.chunks():
                    dest.write(chunk)

            key = f"accesos/{acceso.unidad_id}/{uuid.uuid4()}.jpg"
            upload_file(tmp_path, key)
            os.remove(tmp_path)

            acceso.evidencia_s3 = key
            acceso.save()

        return acceso

    def get_evidencia_url(self, obj):
        if obj.evidencia_s3:
            return get_presigned_url(obj.evidencia_s3, expires_in=300)
        return None

class IncidenteSerializer(serializers.ModelSerializer):
    evidencia = serializers.ImageField(write_only=True, required=False)
    evidencia_url = serializers.SerializerMethodField()

    class Meta:
        model = Incidente
        fields = [
            "id", "unidad", "user", "titulo", "descripcion", "estado",
            "evidencia_s3", "evidencia", "evidencia_url"
        ]
        read_only_fields = ["evidencia_s3"]

    def create(self, validated_data):
        evidencia = validated_data.pop("evidencia", None)
        incidente = super().create(validated_data)

        if evidencia:
            tmp_path = f"/tmp/{uuid.uuid4()}.jpg"
            with open(tmp_path, "wb+") as dest:
                for chunk in evidencia.chunks():
                    dest.write(chunk)

            key = f"incidentes/{incidente.unidad_id}/{uuid.uuid4()}.jpg"
            upload_file(tmp_path, key)
            os.remove(tmp_path)

            incidente.evidencia_s3 = key
            incidente.save()

        return incidente

    def get_evidencia_url(self, obj):
        if obj.evidencia_s3:
            return get_presigned_url(obj.evidencia_s3, expires_in=300)
        return None