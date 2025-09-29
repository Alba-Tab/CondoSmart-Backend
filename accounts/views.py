from django.contrib.auth import update_session_auth_hash
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core.permissions import IsAuth
from core.views import BaseViewSet
from core.services import delete_faces_by_external_id
from .models import CustomUser
from .serializers import UserSerializer, MeSerializer

class MeView(APIView):
    permission_classes = [IsAuth]
    def get(self, request):
        return Response(MeSerializer(request.user).data)

class UserViewSet(BaseViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["is_active", "ci"]
    search_fields = ["username", "ci", "first_name", "last_name"]
    ordering_fields = "__all__"
        
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser: 
            return CustomUser.objects.all()
        else:
            return CustomUser.objects.filter(pk=user.pk)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete(user=request.user)
        delete_faces_by_external_id(f"user_{instance.id}")
        print("💖DELETE user")
        return Response(status=204)
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuth]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"detail": "Faltan campos"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"detail": "Contraseña actual incorrecta"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return Response({"detail": "Contraseña cambiada correctamente"})

