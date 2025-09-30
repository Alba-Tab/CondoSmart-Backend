from django_filters import rest_framework as filters
from core.permissions import IsAuth, AlcancePermission
from core import DefaultPagination
from core.mixins import AlcanceViewSetMixin
from .models import AreaComun, Reserva, Suministro
from .serializers import AreaComunSerializer, ReservaSerializer, SuministroSerializer
from core.views import BaseViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ReservaFilter(filters.FilterSet):
    start_gte = filters.DateTimeFilter(field_name="start", lookup_expr="gte")
    start_lte = filters.DateTimeFilter(field_name="start", lookup_expr="lte")
    end_gte = filters.DateTimeFilter(field_name="end", lookup_expr="gte")
    end_lte = filters.DateTimeFilter(field_name="end", lookup_expr="lte")
    class Meta:
        model = Reserva
        fields = ["unidad","area","status","start_gte","start_lte","end_gte","end_lte"]

class AreaComunViewSet(BaseViewSet):
    queryset = AreaComun.objects.all()
    serializer_class = AreaComunSerializer
    filterset_fields = ["is_active","requires_deposit","name"]
    search_fields = ["name","descripcion"]

class ReservaViewSet(AlcanceViewSetMixin):
    queryset = Reserva.objects.select_related("unidad","area")
    serializer_class = ReservaSerializer
    permission_classes = BaseViewSet.permission_classes + [AlcancePermission]
    filterset_class = ReservaFilter
    search_fields = ["notas"]
    scope_field = "unidad"

    def perform_create(self, serializer):
        reserva = serializer.save()
        reserva.create_cargo_if_required()
        
    @action(detail=True, methods=["post"])
    def confirmar(self, request, pk=None):
        reserva = self.get_object()
        try:
            reserva.confirmar()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": reserva.status})
    
    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        try:
            reserva.cancelar(user=request.user)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": reserva.status})

    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        reserva = self.get_object()
        try:
            reserva.finalizar()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": reserva.status})
    
class SuministroViewSet(BaseViewSet):
    queryset = Suministro.objects.all()
    serializer_class = SuministroSerializer
    permission_classes = BaseViewSet.permission_classes + [AlcancePermission]
    filterset_fields = ["name","descripcion","is_active"]
    search_fields = ["name","descripcion"]
    
