from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)
    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all()
    )
    class Meta:
        model = CustomUser
        fields = ["pk","username","password","first_name","last_name","email",
                  "ci","phone","is_active","groups","is_staff"]
        read_only_fields = ("created_by",)

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        password = validated_data.pop("password", None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        if groups:
            user.groups.set(groups)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["pk","username","ci","first_name","last_name","email","phone","is_active"]
        read_only_fields = ("created_by", "updated_by")