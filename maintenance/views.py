from .serializers import ServicioSerializer, TicketMantenimientoSerializer, TarifaServicioSerializer
from core import IsAuth, AlcancePermission, DefaultPagination
from core.mixins import AlcanceViewSetMixin
from .models import Servicio, TicketMantenimiento, TarifaServicio
from django_filters import rest_framework as filters
from core.views import BaseViewSet
from django.db.models import Q

class TicketFilter(filters.FilterSet):
    # Por qué: alias legibles para rangos y nulos
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

class TarifaFilter(filters.FilterSet):
    vigente_desde_gte = filters.DateFilter(field_name="vigente_desde", lookup_expr="gte")
    vigente_desde_lte = filters.DateFilter(field_name="vigente_desde", lookup_expr="lte")
    vigente_hasta_isnull = filters.BooleanFilter(field_name="vigente_hasta", lookup_expr="isnull")
    vigente_en = VigenteEnFilter(field_name="vigente_desde")

    class Meta:
        model = TarifaServicio
        fields = ["servicio","vigente_desde_gte","vigente_desde_lte","vigente_hasta_isnull","vigente_en"]

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

class TarifaServicioViewSet(BaseViewSet):
    queryset = TarifaServicio.objects.select_related("servicio")
    serializer_class = TarifaServicioSerializer
    permission_classes = [IsAuth]
    filterset_class = TarifaFilter
    ordering_fields = "__all__"
    pagination_class = DefaultPagination