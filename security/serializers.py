from rest_framework import serializers
from core.services import (upload_fileobj, get_presigned_url, 
                           index_face, delete_faces_by_external_id, search_face, 
                           detect_plate)
from .models import Visita, Acceso, Incidente, AccesoEvidencia
from django.utils.timezone import now, timedelta

class VisitaSerializer(serializers.ModelSerializer):
    permitido = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    photo = serializers.ImageField(write_only=True, required=False)
    class Meta:
        model = Visita
        fields = [
            "id", "name", "documento", "telefono", 
            "photo", "photo_key", "photo_url",
            "fecha_inicio", "dias_permiso","is_active",
            "created_at", "updated_at", "permitido"
        ]
        read_only_fields = ["photo_key", "created_at", "updated_at"]
        
    def get_permitido(self, obj):
        inicio = obj.fecha_inicio or obj.created_at
        fin = inicio + timedelta(days=obj.dias_permiso)
        return inicio <= now() <= fin

    def get_photo_url(self, obj):
        if obj.photo_key:
            return get_presigned_url(obj.photo_key, expires_in=300)
        return None
    
    def create(self, validated_data):
        photo = validated_data.pop("photo", None)
        if not validated_data.get("fecha_inicio"):
            validated_data["fecha_inicio"] = now()
        visita = super().create(validated_data)

        if photo:
            key = f"visitas/visita_{visita.id}.jpg"
            upload_fileobj(photo, key)
            index_face(key, f"visita_{visita.id}")
            visita.photo_key = key
            visita.save()

        return visita

    def update(self, instance, validated_data):
        photo = validated_data.pop("photo", None)
        is_active_changed = "is_active" in validated_data
        was_active = getattr(instance, "is_active", False)
        will_be_active = validated_data.get("is_active", was_active)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if photo:
            delete_faces_by_external_id(f"visita_{instance.id}")
            key = f"visitas/visita_{instance.id}.jpg"
            upload_fileobj(photo, key)
            instance.photo_key = key
            if instance.is_active:
                index_face(key, f"visita_{instance.id}")
        elif is_active_changed:
            if not will_be_active:
                delete_faces_by_external_id(f"visita_{instance.id}")
            elif not was_active and will_be_active and instance.photo_key:
                index_face(instance.photo_key, f"visita_{instance.id}")

        instance.save()
        return instance

class AccesoEvidenciaSerializer(serializers.ModelSerializer):
    evidencia = serializers.ImageField(write_only=True, required=False)
    evidencia_url = serializers.SerializerMethodField()
    visita_activa = serializers.SerializerMethodField()

    class Meta:
        model = AccesoEvidencia
        fields = [
            "id", "acceso", "modo", "tipo",
            "user", "visita", "vehiculo",
            "match","is_active",
            "evidencia", "evidencia_s3", "evidencia_url",
            "visita_activa", "created_at", "updated_at", "is_active"
        ]
        read_only_fields = ["evidencia_s3", "match"]

    def create(self, validated_data):
        evidencia = validated_data.pop("evidencia", None)
        modo = validated_data.get("modo")

        acceso_evidencia = super().create(validated_data)

        if evidencia:
            key = f"accesos/{acceso_evidencia.acceso_id}/{modo}_{evidencia.id}.jpg"
            upload_fileobj(evidencia, key)
            acceso_evidencia.evidencia_s3 = key

            # --- Procesamiento según modo ---
            if modo == "face":
                result = search_face(key)
                if result:
                    acceso_evidencia.match = True
                    if result["external_id"].startswith("user_"):
                        acceso_evidencia.tipo = "usuario"
                        acceso_evidencia.user_id = int(result["external_id"].replace("user_", ""))
                    elif result["external_id"].startswith("visita_"):
                        acceso_evidencia.tipo = "externo"
                        acceso_evidencia.visita_id = int(result["external_id"].replace("visita_", ""))
            elif modo == "placa":
                plate = detect_plate(key)
                if plate:
                    from housing.models import Vehiculo
                    vehiculo = Vehiculo.objects.filter(placa=plate).first()
                    if vehiculo:
                        acceso_evidencia.match = True
                        acceso_evidencia.tipo = "vehiculo"
                        acceso_evidencia.vehiculo = vehiculo
                        acceso_evidencia.user = vehiculo.responsable

        acceso_evidencia.save()
        return acceso_evidencia
    
    def update(self, instance, validated_data):
        is_active_changed = "is_active" in validated_data
        will_be_active = validated_data.get("is_active", instance.is_active)

        if is_active_changed and not will_be_active:
            if instance.modo == "face" and instance.evidencia_s3:
                delete_faces_by_external_id(
                    f"visita_{instance.visita.id}" if instance.visita else f"user_{instance.user.id}"
                )
            instance.delete()
            return None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def get_evidencia_url(self, obj):
        if obj.evidencia_s3:
            return get_presigned_url(obj.evidencia_s3, expires_in=300)
        return None
    
    def get_visita_activa(self, obj):
        return obj.visita.is_active if obj.visita else None
    
class AccesoSerializer(serializers.ModelSerializer):
    evidencias = AccesoEvidenciaSerializer(many=True, read_only=True)

    class Meta:
        model = Acceso
        fields = ["id", "unidad", "sentido", "permitido","is_active", "created_at", "evidencias"]
        read_only_fields = ["created_at"]

class IncidenteSerializer(serializers.ModelSerializer):
    evidencia = serializers.ImageField(write_only=True, required=False)
    evidencia_url = serializers.SerializerMethodField()

    class Meta:
        model = Incidente
        fields = [
            "id", "unidad", "user", "titulo", "descripcion", "estado","is_active",
            "evidencia_s3", "evidencia", "evidencia_url"
        ]
        read_only_fields = ["evidencia_s3"]

    def create(self, validated_data):
        evidencia = validated_data.pop("evidencia", None)
        incidente = super().create(validated_data)

        if evidencia:
            key = f"incidentes/incidente_{incidente.id}.jpg"
            upload_fileobj(evidencia, key)   
            incidente.evidencia_s3 = key
            incidente.save()

        return incidente

    def update(self, instance, validated_data):
        evidencia = validated_data.pop("evidencia", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if evidencia:
            key = f"incidentes/incidente_{instance.id}.jpg"
            upload_fileobj(evidencia, key)
            instance.evidencia_s3 = key

        instance.save()
        return instance

    def get_evidencia_url(self, obj):
        if obj.evidencia_s3:
            return get_presigned_url(obj.evidencia_s3, expires_in=300)
        return None