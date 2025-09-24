from rest_framework import viewsets
from django_filters import rest_framework as filters
from core.permissions import IsAuth
from core.pagination import DefaultPagination
from .models import Visita, Acceso, Incidente
from .serializers import VisitaSerializer, AccesoSerializer, IncidenteSerializer

class AccesoFilter(filters.FilterSet):
    fecha_gte = filters.DateTimeFilter(field_name="fecha", lookup_expr="gte")
    fecha_lte = filters.DateTimeFilter(field_name="fecha", lookup_expr="lte")
    fecha_exacta = filters.DateFilter(field_name="fecha", lookup_expr="date")
    class Meta:
        model = Acceso
        fields = ["unidad","tipo","modo","sentido","fecha","fecha_gte","fecha_lte","fecha_exacta"]

class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["user","documento","created_at","updated_at"]
    search_fields = ["nombre","documento","telefono"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class AccesoViewSet(viewsets.ModelViewSet):
    queryset = Acceso.objects.select_related("unidad","visita")
    serializer_class = AccesoSerializer
    permission_classes = [IsAuth]
    filterset_class = AccesoFilter
    search_fields = ["visita__nombre","visita__documento","modo","tipo","sentido"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class IncidenteViewSet(viewsets.ModelViewSet):
    queryset = Incidente.objects.select_related("unidad")
    serializer_class = IncidenteSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["unidad","user","estado","created_at","updated_at"]
    search_fields = ["titulo","descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination