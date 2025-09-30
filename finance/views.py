from django_filters import rest_framework as filters
from core import IsAuth, AlcancePermission, DefaultPagination
from core.mixins import AlcanceViewSetMixin
from .models import Cargo, Pago, PagoCargo
from .serializers import CargoSerializer, PagoSerializer, PagoCargoSerializer
from core.views import BaseViewSet
from rest_framework.decorators import action

class PagoFilter(filters.FilterSet):
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
    queryset = Pago.objects.select_related("user")
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
    @action(detail=True, methods=["post"])
    def confirmar(self, request, pk=None):
        pago = self.get_object()
        try:
            pago.confirmar()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(PagoSerializer(pago).data)

    @action(detail=True, methods=["post"])
    def fallido(self, request, pk=None):
        pago = self.get_object()
        pago.marcar_fallido()
        return Response(PagoSerializer(pago).data)

class PagoCargoViewSet(AlcanceViewSetMixin):
    queryset = PagoCargo.all_objects.all()
    serializer_class = PagoCargoSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["pago", "cargo", "monto", "orden", "created_at", "updated_at"]
    search_fields = ["pago__user__username", "cargo__descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "cargo__unidad"
