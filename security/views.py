from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from django_filters import rest_framework as dj_filters
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import IsAuth, AlcancePermission
from core.pagination import DefaultPagination
from core.services import delete_faces_by_external_id
from core.mixins import AlcanceViewSetMixin
from core.views import BaseViewSet
from .models import Visita, Acceso, Incidente, AccesoEvidencia
from .serializers import VisitaSerializer, AccesoSerializer, IncidenteSerializer, AccesoEvidenciaSerializer

class VisitaViewSet(BaseViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["user","documento","created_at","updated_at"]
    search_fields = ["nombre","documento","telefono"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete(user=request.user)
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
    search_fields = ["unidad__nombre", "unidad__code"]
    ordering_fields = "__all__"
    ordering = ["-created_at"]
    pagination_class = DefaultPagination

class AccesoEvidenciaViewSet(BaseViewSet):
    queryset = AccesoEvidencia.objects.select_related("acceso", "user", "visita", "vehiculo")
    serializer_class = AccesoEvidenciaSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["acceso", "acceso__unidad", "modo", "tipo", "match", "created_at"]
    search_fields = ["user__username", "vehiculo__placa", "visita__nombre"]
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
    
