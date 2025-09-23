
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_doc = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username_or_doc, password=password)
        if not user:
            try:
                u = User.objects.get(document_id=username_or_doc)
            except User.DoesNotExist:
                raise serializers.ValidationError({"detail":"Credenciales inválidas"})
            user = authenticate(username=u.username, password=password)
            if not user:
                raise serializers.ValidationError({"detail":"Credenciales inválidas"})
        data = super().validate({"username": user.username, "password": password})
        data["user"] = {# type: ignore
            "id": user.id,# type: ignore
            "username": user.username,
            "document_id": user.document_id,# type: ignore
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer