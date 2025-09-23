from rest_framework import serializers
from .models import CustomUser, Rol

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)

    class Meta:
        model = CustomUser
        fields = ["id","username","password","first_name","last_name","email",
                  "document_id","phone","is_active","is_staff"]
        read_only_fields = ["is_staff"] 

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"    

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","username","id_document","first_name","last_name","email","phone","is_active"]