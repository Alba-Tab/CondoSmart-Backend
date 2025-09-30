from .serializers import ServicioSerializer, TicketMantenimientoSerializer
from core import IsAuth, AlcancePermission, DefaultPagination
from core.mixins import AlcanceViewSetMixin
from .models import Servicio, TicketMantenimiento
from django_filters import rest_framework as filters
from core.views import BaseViewSet
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation

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
        monto_str = request.data.get('monto')
        if not monto_str:
            return Response(
                {"error": "El campo 'monto' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1. Convierte el string a Decimal aquí, en la vista.
            monto = Decimal(monto_str)
            if monto <= 0:
                raise ValueError("El monto debe ser un número positivo.")

            # 2. Pasa el objeto Decimal al método del modelo.
            cargo = ticket.generar_cargo(monto=monto, user=request.user)

            # 3. Devuelve el ticket actualizado para mostrar el nuevo precio.
            ticket_serializer = self.get_serializer(ticket)
            return Response(ticket_serializer.data, status=status.HTTP_201_CREATED)

        # 4. Captura errores de conversión (ej. "abc") y de lógica (ej. monto negativo).
        except (ValueError, InvalidOperation) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        ticket = self.get_object()
        try:
            ticket.cancelar_ticket(user=request.user)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": ticket.estado})