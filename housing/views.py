from .models import Unidad, Residency, Vehiculo, Mascota, Contrato
from .serializers import UnidadSerializer, ResidencySerializer, VehiculoSerializer, MascotaSerializer, ContratoSerializer
from core.permissions import IsAuth, AlcancePermission
from core.pagination import DefaultPagination
from core.mixins import AlcanceViewSetMixin
from core.views import BaseViewSet
class UnidadViewSet(AlcanceViewSetMixin):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["is_active", "code","user", "created_at", "updated_at"]
    search_fields = ["code","user"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "id" 

class ResidencyViewSet(AlcanceViewSetMixin):
    queryset = Residency.objects.select_related("user","unidad")
    serializer_class = ResidencySerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["user","unidad","is_owner","tipo_ocupacion","status","start","end"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "unidad"

class VehiculoViewSet(BaseViewSet):
    queryset = Vehiculo.objects.select_related("unidad","responsable")
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["unidad","placa","marca","color","responsable"]
    search_fields = ["placa","marca","color"]
    ordering_fields = "__all__"
    scope_field = "unidad"
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(responsable=self.request.user)
    
class MascotaViewSet(BaseViewSet):
    queryset = Mascota.objects.select_related("unidad","responsable")
    serializer_class = MascotaSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["unidad","tipo","activo","desde","hasta","responsable"]
    search_fields = ["nombre","raza"]
    ordering_fields = "__all__"
    scope_field = "unidad"
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(responsable=self.request.user)
    
class ContratoViewSet(AlcanceViewSetMixin):
    
    queryset = Contrato.objects.select_related("unidad","inquilino")
    serializer_class = ContratoSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["unidad","inquilino","duenno","activo","start","end"]
    ordering_fields = "__all__"
    scope_field = "unidad"
    