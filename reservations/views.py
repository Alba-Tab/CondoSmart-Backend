from rest_framework import viewsets
from django_filters import rest_framework as filters
from core.permissions import IsAuth
from core.pagination import DefaultPagination
from .models import AreaComun, Reserva, ReservaSuministro, Suministro
from .serializers import AreaComunSerializer, ReservaSerializer, ReservaSuministroSerializer, SuministroSerializer

class ReservaFilter(filters.FilterSet):
    start_gte = filters.DateTimeFilter(field_name="start", lookup_expr="gte")
    start_lte = filters.DateTimeFilter(field_name="start", lookup_expr="lte")
    end_gte = filters.DateTimeFilter(field_name="end", lookup_expr="gte")
    end_lte = filters.DateTimeFilter(field_name="end", lookup_expr="lte")
    class Meta:
        model = Reserva
        fields = ["unidad","area","status","start_gte","start_lte","end_gte","end_lte"]

class AreaComunViewSet(viewsets.ModelViewSet):
    queryset = AreaComun.objects.all()
    serializer_class = AreaComunSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["is_active","requires_deposit","name"]
    search_fields = ["name","descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related("unidad","area")
    serializer_class = ReservaSerializer
    permission_classes = [IsAuth]
    filterset_class = ReservaFilter
    search_fields = ["notas"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class SuministroViewSet(viewsets.ModelViewSet):
    queryset = Suministro.objects.all()
    serializer_class = SuministroSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["name","descripcion","is_active"]
    search_fields = ["name","descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    
class ReservaSuministroViewSet(viewsets.ModelViewSet):
    queryset = ReservaSuministro.objects.select_related("reserva","suministro")
    serializer_class = ReservaSuministroSerializer
    permission_classes = [IsAuth]
    filterset_fields = ["reserva","suministro","cantidad"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination