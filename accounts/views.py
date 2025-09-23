
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsAuth, IsAdmin
from .models import CustomUser, Rol
from .serializers import UserSerializer, RolSerializer, PasswordChangeSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["is_active", "document_id"]
    search_fields = ["username", "document_id", "first_name", "last_name", "id_document"]
    ordering_fields = "__all__"
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomUser.objects.all()
        else:
            return CustomUser.objects.filter(id=user.id)

class PasswordChangeView(APIView):
    permission_classes = [IsAuth]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": "Contraseña actual incorrecta."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Contraseña cambiada correctamente."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.select_related("user")
    serializer_class = RolSerializer
    permission_classes = [IsAuth, IsAdmin]
    filterset_fields = ["user", "group_name"]
    ordering_fields = "__all__"