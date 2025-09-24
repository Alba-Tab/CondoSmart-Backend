from rest_framework import viewsets
from .models import Unidad, Residency, Vehiculo, Mascota, Contrato
from .serializers import UnidadSerializer, ResidencySerializer, VehiculoSerializer, MascotaSerializer, ContratoSerializer
from core.permissions import IsAuth, IsAdmin, IsResident
from core.pagination import DefaultPagination

class UnidadViewSet(viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["is_active", "code","user", "created_at", "updated_at"]
    search_fields = ["code","user"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class ResidencyViewSet(viewsets.ModelViewSet):
    queryset = Residency.objects.select_related("user","unidad")
    serializer_class = ResidencySerializer
    permission_classes = [IsAuth]
    filterset_fields = ["user","unidad","is_owner","tipo_ocupacion","status","start","end"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.select_related("unidad","responsable")
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["unidad","placa","marca","color","responsable"]
    search_fields = ["placa","marca","color"]
    ordering_fields = "__all__"
    
class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.select_related("unidad","responsable")
    serializer_class = MascotaSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["unidad","tipo","activo","desde","hasta","responsable"]
    search_fields = ["nombre","raza"]
    ordering_fields = "__all__"
    
class ContratoViewSet(viewsets.ModelViewSet):
    
    queryset = Contrato.objects.select_related("unidad","inquilino")
    serializer_class = ContratoSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["unidad","inquilino","duenno","activo","start","end"]
    ordering_fields = "__all__"
    