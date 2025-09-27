from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser
from core.services import upload_file, get_presigned_url
import uuid, os

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)
    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all()
    )

    photo = serializers.ImageField(write_only=True, required=False)
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            "pk", "username", "password", "first_name", "last_name",
            "email", "ci", "phone", "is_active", "groups", "is_staff",
            "photo_key", "photo", "photo_url"
        ]
        read_only_fields = ("created_by", "photo_key")

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        password = validated_data.pop("password", None)
        photo = validated_data.pop("photo", None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        if groups:
            user.groups.set(groups)
        if photo:
            tmp_path = f"/tmp/{uuid.uuid4()}.jpg"
            with open(tmp_path, "wb+") as dest:
                for chunk in photo.chunks():
                    dest.write(chunk)

            key = f"usuarios/{user.pk}/foto.jpg"
            upload_file(tmp_path, key)
            os.remove(tmp_path)

            user.photo_key = key
            user.save()  # Guarda el cambio de photo_key
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        photo = validated_data.pop("photo", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if photo:
            tmp_path = f"/tmp/{uuid.uuid4()}.jpg"
            with open(tmp_path, "wb+") as dest:
                for chunk in photo.chunks():
                    dest.write(chunk)

            key = f"usuarios/{instance.pk}/foto.jpg"
            upload_file(tmp_path, key)
            os.remove(tmp_path)

            instance.photo_key = key
            instance.save()

        return instance
    
    def get_photo_url(self, obj):
        if obj.photo_key:
            return get_presigned_url(obj.photo_key, expires_in=300)
        return None

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["pk","username","ci","first_name","last_name","email","phone","is_active"]
        read_only_fields = ("created_by", "updated_by")