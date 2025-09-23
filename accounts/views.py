from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsAuth, IsAdmin
from .models import CustomUser, Rol
from .serializers import UserSerializer, RolSerializer, MeSerializer

class MeView(APIView):
    permission_classes = [IsAuth]
    def get(self, request):
        return Response(MeSerializer(request.user).data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["is_active", "document_id"]
    search_fields = ["username", "document_id", "first_name", "last_name"]
    ordering_fields = "__all__"
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomUser.objects.all()
        else:
            return CustomUser.objects.filter(id=user.id) # type: ignore

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.select_related("user")
    serializer_class = RolSerializer
    permission_classes = [IsAuth, IsAdmin]
    filterset_fields = ["user", "group_name"]
    ordering_fields = "__all__"