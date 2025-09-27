from django_filters import rest_framework as filters
from core.permissions import IsAuth, AlcancePermission
from core.pagination import DefaultPagination
from .models import Cargo, Pago, PagoCargo
from .serializers import CargoSerializer, PagoSerializer, PagoCargoSerializer
from core.mixins import AlcanceViewSetMixin
from core.views import BaseViewSet

class PagoFilter(filters.FilterSet):
    # aliases amigables
    fecha_gte = filters.DateTimeFilter(field_name="fecha", lookup_expr="gte")
    fecha_lte = filters.DateTimeFilter(field_name="fecha", lookup_expr="lte")

    class Meta:
        model = Pago
        fields = ["user", "estado", "fecha_gte", "fecha_lte", "comprobante_key"]
        
class CargoViewSet(AlcanceViewSetMixin):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["unidad","concepto", "descripcion", "periodo","monto", "estado", "created_at", "updated_at"]
    search_fields = ["descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class PagoViewSet(BaseViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuth]
    filterset_class = PagoFilter
    search_fields = ["user__username", "observacion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    # Admin ve todos, usuario ve solo los suyos
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

class PagoCargoViewSet(AlcanceViewSetMixin):
    queryset = PagoCargo.objects.all()
    serializer_class = PagoCargoSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["pago", "cargo", "monto", "orden", "created_at", "updated_at"]
    search_fields = ["pago__user__username", "cargo__descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "cargo__unidad"
