from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser
from core.services import upload_fileobj, get_presigned_url, index_face, delete_faces_by_external_id

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
            "photo_key", "photo", "photo_url", "is_deleted"
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
            key = f"usuarios/user_{user.pk}.jpg"
            upload_fileobj(photo, key)
            user.photo_key = key
            user.save()
            index_face(key, external_id=f"user_{user.pk}")
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop("groups", None)
        password = validated_data.pop("password", None)
        photo = validated_data.pop("photo", None)
        
        is_deleted_changed = "is_deleted" in validated_data
        was_deleted = getattr(instance, "is_deleted", False) # estado previo
        will_be_deleted = validated_data.get("is_deleted", was_deleted) # estado nuevo
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if groups is not None:
            instance.groups.set(groups)

        if password:
            instance.set_password(password)
            
        
        if photo:
            delete_faces_by_external_id(f"user_{instance.pk}")
            key = f"usuarios/user_{instance.pk}.jpg"
            upload_fileobj(photo, key)
            instance.photo_key = key
            index_face(key, f"user_{instance.pk}")
        elif is_deleted_changed:
            if will_be_deleted:
                delete_faces_by_external_id(f"user_{instance.pk}")
            elif was_deleted and not will_be_deleted and instance.photo_key:
                index_face(instance.photo_key, f"user_{instance.pk}")

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