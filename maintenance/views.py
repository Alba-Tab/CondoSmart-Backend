from .serializers import ServicioSerializer, TicketMantenimientoSerializer
from core import IsAuth, AlcancePermission, DefaultPagination
from core.mixins import AlcanceViewSetMixin
from .models import Servicio, TicketMantenimiento
from django_filters import rest_framework as filters
from core.views import BaseViewSet
from django.db.models import Q
from rest_framework.decorators import action

class TicketFilter(filters.FilterSet):
    programado_gte = filters.DateTimeFilter(field_name="programado", lookup_expr="gte")
    programado_lte = filters.DateTimeFilter(field_name="programado", lookup_expr="lte")
    cerrado_isnull = filters.BooleanFilter(field_name="cerrado", lookup_expr="isnull")

    class Meta:
        model = TicketMantenimiento
        fields = ["unidad","servicio","estado","programado_gte","programado_lte","cerrado_isnull"]

class VigenteEnFilter(filters.Filter):
    """Por qué: filtrar tarifas vigentes en una fecha específica."""
    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(vigente_desde__lte=value).filter(
            Q(vigente_hasta__isnull=True) | Q(vigente_hasta__gte=value))

class ServicioViewSet(BaseViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["is_active","name"]
    search_fields = ["name","descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class TicketMantenimientoViewSet(AlcanceViewSetMixin):
    queryset = TicketMantenimiento.objects.select_related("unidad","servicio")
    serializer_class = TicketMantenimientoSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_class = TicketFilter
    search_fields = ["titulo","descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "unidad"

    @action(detail=True, methods=["post"])
    def generar_cargo(self, request, pk=None):
        ticket = self.get_object()
        try:
            cargo = ticket.generar_cargo()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "cargo_id": cargo.id,
            "unidad": ticket.unidad.id,
            "precio": str(ticket.precio),
            "estado": cargo.estado,
        })