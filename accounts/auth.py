
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from rest_framework.views import APIView
from core.permissions import IsAuth
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            try:
                u = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError({"detail":"Credenciales inválidas"})
            user = authenticate(username=u.username, password=password)
            if not user:
                raise serializers.ValidationError({"detail":"Credenciales inválidas"})
        data = super().validate({"username": user.username, "password": password})
        data["user"] = {# type: ignore
            "pk": user.pk,
            "username": user.username,
            "ci": user.ci, # type: ignore
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class LogoutView(APIView):
    permission_classes = [IsAuth]

    def post(self, request):
        # cliente debe enviar {"refresh": "<refresh_token>"}
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail":"refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail":"invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Sesión cerrada"}, status=status.HTTP_200_OK)