
from rest_framework.response import Response
from rest_framework import filters, status 
from django_filters import rest_framework as dj_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from core import IsAuth, AlcancePermission, DefaultPagination
from core.services import delete_faces_by_external_id
from core.mixins import AlcanceViewSetMixin
from core.views import BaseViewSet
from .models import Visita, Acceso, Incidente, AccesoEvidencia
from .serializers import VisitaSerializer, AccesoSerializer, IncidenteSerializer, AccesoEvidenciaSerializer
from decimal import Decimal


class VisitaViewSet(BaseViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [IsAuth]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active", "documento", "created_at", "updated_at"]
    search_fields = ["name", "documento", "telefono"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

    def get_queryset(self):
        qs = super().get_queryset()
        # Si no es staff, filtra solo visitas activas creadas por el usuario
        if self.request.user.is_staff:
            return qs
        return qs.filter(created_by=self.request.user, is_active=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        delete_faces_by_external_id(f"visita_{instance.id}")
        return Response(status=204)
    
class AccesoFilter(dj_filters.FilterSet):
    created_gte = dj_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_lte = dj_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    created_date = dj_filters.DateFilter(field_name="created_at", lookup_expr="date")

    class Meta:
        model = Acceso
        fields = ["unidad", "sentido", "permitido", "created_gte", "created_lte", "created_date"]

class AccesoViewSet(AlcanceViewSetMixin):
    queryset = Acceso.objects.select_related("unidad")
    serializer_class = AccesoSerializer
    permission_classes = [IsAuth, AlcancePermission]

    filter_backends = [dj_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AccesoFilter
    search_fields = ["unidad__name", "unidad__code"]
    ordering_fields = "__all__"
    ordering = ["-created_at"]
    pagination_class = DefaultPagination

class AccesoEvidenciaViewSet(BaseViewSet):
    queryset = AccesoEvidencia.objects.select_related("acceso", "user", "visita", "vehiculo")
    serializer_class = AccesoEvidenciaSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["acceso", "acceso__unidad", "modo", "tipo", "match", "created_at"]
    search_fields = ["user__username", "vehiculo__placa", "visita__name"]
    ordering_fields = "__all__"
    ordering = ["-created_at"]
    pagination_class = DefaultPagination


class IncidenteViewSet(AlcanceViewSetMixin):
    queryset = Incidente.objects.select_related("unidad")
    serializer_class = IncidenteSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["unidad", "user", "estado", "created_at", "updated_at"]
    search_fields = ["titulo", "descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "unidad"
    
    @action(detail=True, methods=["post"])
    def generar_cargo(self, request, pk=None):
        incidente = self.get_object()
        monto = request.data.get("monto")
        if not monto:
            return Response({"error": "Debe indicar el monto de la multa"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cargo = incidente.generar_cargo(Decimal(monto))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "cargo_id": cargo.id,
            "estado": cargo.estado,
            "saldo": str(cargo.saldo),
        })
    
