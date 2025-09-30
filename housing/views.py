from .models import Unidad, Residency, Vehiculo, Mascota, Contrato
from .serializers import UnidadSerializer, ResidencySerializer, VehiculoSerializer, MascotaSerializer, ContratoSerializer
from core import IsAuth, AlcancePermission, DefaultPagination
from core.mixins import AlcanceViewSetMixin
from core.views import BaseViewSet
from rest_framework import serializers
from core.services import get_presigned_url
from django_filters import rest_framework as filters

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
    queryset = Mascota.objects.select_related("responsable")
    serializer_class = MascotaSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["tipo","is_active","desde","hasta","responsable"]
    search_fields = ["name","raza"]
    ordering_fields = "__all__"
    scope_field = "responsable"
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(responsable=self.request.user)

class ContratoFilter(filters.FilterSet):
    start_gte = filters.DateFilter(field_name="start", lookup_expr="gte")
    start_lte = filters.DateFilter(field_name="start", lookup_expr="lte")
    end_gte = filters.DateFilter(field_name="end", lookup_expr="gte")
    end_lte = filters.DateFilter(field_name="end", lookup_expr="lte")

    class Meta:
        model = Contrato
        fields = ["unidad", "duenno", "inquilino", "is_active", "start_gte", "start_lte", "end_gte", "end_lte"]


class ContratoViewSet(AlcanceViewSetMixin):
    queryset = Contrato.all_objects.select_related("unidad", "duenno", "inquilino").all()
    serializer_class = ContratoSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_class = ContratoFilter
    search_fields = ["descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    def get_documento_url(self, obj):
        if obj.documento:
            return get_presigned_url(obj.documento.name, expires_in=300)
        return None
    