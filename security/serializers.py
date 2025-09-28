from rest_framework import serializers
from core.services import upload_fileobj, upload_file, get_presigned_url
import uuid, os
from .models import Visita, Acceso, Incidente

class VisitaSerializer(serializers.ModelSerializer):
    # Campo solo para recibir archivo en POST
    foto = serializers.ImageField(write_only=True, required=False)
    # Campo solo de salida
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Visita
        fields = [
            "id", "nombre", "documento", "telefono",
            "user", "photo_key", "foto", "foto_url"
        ]
        read_only_fields = ["photo_key"]

    def create(self, validated_data):
        foto = validated_data.pop("foto", None)
        visita = super().create(validated_data)

        if foto:
            key = f"visitas/{visita.id}/foto_{uuid.uuid4()}.jpg"
            upload_fileobj(foto, key)   # directo, sin /tmp
            visita.photo_key = key
            visita.save()

        return visita

    def update(self, instance, validated_data):
        foto = validated_data.pop("foto", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if foto:
            key = f"visitas/{instance.id}/foto_{uuid.uuid4()}.jpg"
            upload_fileobj(foto, key)
            instance.photo_key = key

        instance.save()
        return instance

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
            key = f"accesos/{acceso.unidad_id}/{uuid.uuid4()}.jpg"
            upload_fileobj(evidencia, key)   # directo en memoria
            acceso.evidencia_s3 = key
            acceso.save()

        return acceso

    def update(self, instance, validated_data):
        evidencia = validated_data.pop("evidencia", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if evidencia:
            key = f"accesos/{instance.unidad_id}/{uuid.uuid4()}.jpg"
            upload_fileobj(evidencia, key)
            instance.evidencia_s3 = key

        instance.save()
        return instance

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
            key = f"incidentes/{incidente.unidad_id}/{uuid.uuid4()}.jpg"
            upload_fileobj(evidencia, key)   # directo en memoria
            incidente.evidencia_s3 = key
            incidente.save()

        return incidente

    def update(self, instance, validated_data):
        evidencia = validated_data.pop("evidencia", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if evidencia:
            key = f"incidentes/{instance.unidad_id}/{uuid.uuid4()}.jpg"
            upload_fileobj(evidencia, key)
            instance.evidencia_s3 = key

        instance.save()
        return instance

    def get_evidencia_url(self, obj):
        if obj.evidencia_s3:
            return get_presigned_url(obj.evidencia_s3, expires_in=300)
        return None