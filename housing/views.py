from .models import Unidad, Residency, Vehiculo, Mascota, Contrato, Condominio
from .serializers import UnidadSerializer, ResidencySerializer, VehiculoSerializer, MascotaSerializer, ContratoSerializer, CondominioSerializer
from core import IsAuth, AlcancePermission, DefaultPagination
from core.mixins import AlcanceViewSetMixin
from core.views import BaseViewSet
from rest_framework import serializers
from core.services import get_presigned_url
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date
from django.db import models
from django.contrib.contenttypes.models import ContentType
from finance.models import Cargo
from decimal import Decimal

class CondominioViewSet(AlcanceViewSetMixin):

    queryset = Condominio.objects.all()
    serializer_class = CondominioSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["is_active", "name", "created_at", "updated_at"]
    search_fields = ["name"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "id"

class UnidadViewSet(AlcanceViewSetMixin):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["is_active", "code","user", "created_at", "updated_at"]
    search_fields = ["code","user"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "id" 

class ResidencyViewSet(AlcanceViewSetMixin):
    queryset = Residency.objects.select_related("user","unidad")
    serializer_class = ResidencySerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["user","unidad","is_owner","tipo_ocupacion","status","start","end"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "unidad"

class VehiculoViewSet(BaseViewSet):
    queryset = Vehiculo.objects.select_related("unidad","responsable")
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["unidad","placa","marca","color","responsable"]
    search_fields = ["placa","marca","color"]
    ordering_fields = "__all__"
    scope_field = "unidad"
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(responsable=self.request.user)
    
class MascotaViewSet(BaseViewSet):
    queryset = Mascota.objects.select_related("responsable")
    serializer_class = MascotaSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["tipo","is_active","desde","hasta","responsable"]
    search_fields = ["name","raza"]
    ordering_fields = "__all__"
    scope_field = "responsable"
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(responsable=self.request.user)

class ContratoFilter(filters.FilterSet):
    start_gte = filters.DateFilter(field_name="start", lookup_expr="gte")
    start_lte = filters.DateFilter(field_name="start", lookup_expr="lte")
    end_gte = filters.DateFilter(field_name="end", lookup_expr="gte")
    end_lte = filters.DateFilter(field_name="end", lookup_expr="lte")

    class Meta:
        model = Contrato
        fields = ["unidad", "duenno", "inquilino", "is_active", "start_gte", "start_lte", "end_gte", "end_lte"]


class ContratoViewSet(AlcanceViewSetMixin):
    queryset = Contrato.all_objects.select_related("unidad", "duenno", "inquilino").all()
    serializer_class = ContratoSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_class = ContratoFilter
    search_fields = ["descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "unidad"
    
    @action(detail=True, methods=["post"])
    def generar_cargo(self, request, pk=None):
        contrato = self.get_object()
        periodo = request.data.get("periodo")
        if not periodo:
            return Response({"error": "Debe enviar un periodo (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from datetime import datetime
            periodo_date = datetime.strptime(periodo, "%Y-%m-%d").date()
            cargo = contrato.generar_cargo_mensual(periodo_date)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "cargo_id": cargo.id,
            "unidad": contrato.unidad.id,
            "periodo": str(cargo.periodo),
            "monto": str(cargo.monto),
            "estado": cargo.estado,
        })
    @action(detail=False, methods=["post"])
    def generar_cargos_mes(self, request):
        hoy = date.today()
        periodo = date(hoy.year, hoy.month, 1)
        print("Generando cargos para el período:", periodo)
        contratos_activos = Contrato.objects.filter(
            is_active=True,
            start__lte=periodo
        ).filter(
            models.Q(end__isnull=True) | models.Q(end__gte=periodo)
        )
        # 2. Obtener los IDs de los contratos que YA tienen un cargo para este período
        content_type = ContentType.objects.get_for_model(Contrato)
        contratos_con_cargo_existente = Cargo.objects.filter(
            content_type=content_type,
            object_id__in=contratos_activos.values_list('id', flat=True),
            periodo=periodo
        ).values_list('object_id', flat=True)

        # 3. Filtrar los contratos a los que realmente les falta el cargo
        contratos_a_generar = contratos_activos.exclude(id__in=contratos_con_cargo_existente)

        nuevos_cargos = []
        for contrato in contratos_a_generar:
            monto = contrato.monto_mensual or Decimal("0.00")
            nuevos_cargos.append(
                Cargo(
                    unidad=contrato.unidad,
                    origen=contrato,
                    concepto="cuota",
                    descripcion=f"Expensa mensual {periodo:%Y-%m} (Contrato {contrato.pk})",
                    monto=monto,
                    saldo=monto,
                    periodo=periodo,
                    created_by=request.user,
                )
            )
        if nuevos_cargos:
            cargos_creados = Cargo.objects.bulk_create(nuevos_cargos)
            cargos_ids = [cargo.pk for cargo in cargos_creados]
        else:
            cargos_ids = []

        return Response({
            "total_generados": len(nuevos_cargos),
            "cargos_ids": cargos_ids,
            "periodo": str(periodo)
        })
          
    def get_documento_url(self, obj):
        if obj.documento:
            return get_presigned_url(obj.documento.name, expires_in=300)
        return None
    