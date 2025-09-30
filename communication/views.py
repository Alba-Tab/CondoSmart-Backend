from django_filters import rest_framework as filters
from core import IsAuth, DefaultPagination
from .models import Comunicado, Notificacion
from .serializers import ComunicadoSerializer, NotificacionSerializer
from rest_framework import decorators, response, status
from django.utils import timezone
from core.views import BaseViewSet

class ComunicadoFilter(filters.FilterSet):
    publicado_gte = filters.DateTimeFilter(field_name="publicado_at", lookup_expr="gte")
    publicado_lte = filters.DateTimeFilter(field_name="publicado_at", lookup_expr="lte")
    class Meta:
        model = Comunicado
        fields = ["publicado_gte","publicado_lte"]

class ComunicadoViewSet(BaseViewSet):
    queryset = Comunicado.objects.all()
    serializer_class = ComunicadoSerializer
    permission_classes = [IsAuth]
    filterset_class = ComunicadoFilter
    search_fields = ["titulo","cuerpo","publicado_at"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class NotificacionFilter(filters.FilterSet):
    publicado_gte = filters.DateTimeFilter(field_name="publicado_at", lookup_expr="gte")
    publicado_lte = filters.DateTimeFilter(field_name="publicado_at", lookup_expr="lte")
    leido_isnull = filters.BooleanFilter(field_name="leido_at", lookup_expr="isnull")
    class Meta:
        model = Notificacion
        fields = ["user","comunicado","publicado_gte","publicado_lte","leido_isnull"]

class NotificacionViewSet(BaseViewSet):
    queryset = Notificacion.objects.select_related("user","comunicado")
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuth]
    filterset_class = NotificacionFilter
    search_fields = ["titulo","cuerpo","tipo","referencia_id"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    
    @decorators.action(detail=True, methods=["post"])
    def leer(self, request, pk=None):
        """Por qué: marcar lectura desde servidor con timestamp confiable."""
        notif = self.get_object()
        notif.leido_at = timezone.now()
        notif.save(update_fields=["leido_at","updated_at"])
        return response.Response({"status": "ok", "leido_at": notif.leido_at}, status=status.HTTP_200_OK)