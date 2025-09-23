from rest_framework import viewsets
from .models import Unidad, Residency
from .serializers import UnidadSerializer, ResidencySerializer
from core.permissions import IsAuth
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from core.pagination import DefaultPagination

class UnidadViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        qs = Unidad.objects.all().prefetch_related("residentes")
        if user.is_staff or user.roles.filter(group_name='guard').exists():
            return qs
        elif user.roles.filter(group_name='resident').exists():
            return qs.filter(residentes__user=user, residentes__end__isnull=True)
        return Unidad.objects.none()
    serializer_class = UnidadSerializer
    permission_classes = [IsAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active", "code"]
    search_fields = ["code"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination

class ResidencyViewSet(viewsets.ModelViewSet):
    #queryset = Residency.objects.select_related("user","unidad")
    serializer_class = ResidencySerializer
    permission_classes = [IsAuth]
    filterset_fields = ["user","unidad","is_owner","start","end"]
    ordering_fields = "__all__"
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.roles.filter(group_name='guard').exists():
            return Residency.objects.select_related("user", "unidad")
        elif user.roles.filter(group_name='resident').exists():
            # Busca las unidades donde el usuario es residente activo
            unidades_usuario = Unidad.objects.filter(residentes__user=user, residentes__end__isnull=True)
            # Devuelve todas las residencias de esas unidades
            return Residency.objects.select_related("user", "unidad").filter(unidad__in=unidades_usuario)
        return Residency.objects.none()
    pagination_class = DefaultPagination