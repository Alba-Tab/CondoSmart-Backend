from django_filters import rest_framework as filters
from core.permissions import IsAuth, AlcancePermission
from core.pagination import DefaultPagination
from core.mixins import AlcanceViewSetMixin
from .models import Visita, Acceso, Incidente
from .serializers import VisitaSerializer, AccesoSerializer, IncidenteSerializer
from core.views import BaseViewSet

from core.services import upload_file
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

import uuid, os

class AccesoFilter(filters.FilterSet):
    fecha_gte = filters.DateTimeFilter(field_name="fecha", lookup_expr="gte")
    fecha_lte = filters.DateTimeFilter(field_name="fecha", lookup_expr="lte")
    fecha_exacta = filters.DateFilter(field_name="fecha", lookup_expr="date")
    class Meta:
        model = Acceso
        fields = ["unidad","tipo","modo","sentido","fecha","fecha_gte","fecha_lte","fecha_exacta"]

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

class AccesoViewSet(AlcanceViewSetMixin):
    queryset = Acceso.objects.select_related("unidad","visita")
    serializer_class = AccesoSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_class = AccesoFilter
    search_fields = ["visita__nombre","visita__documento","modo","tipo","sentido"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "unidad"

class IncidenteViewSet(AlcanceViewSetMixin):
    queryset = Incidente.objects.select_related("unidad")
    serializer_class = IncidenteSerializer
    permission_classes = [IsAuth, AlcancePermission]
    filterset_fields = ["unidad","user","estado","created_at","updated_at"]
    search_fields = ["titulo","descripcion"]
    ordering_fields = "__all__"
    pagination_class = DefaultPagination
    scope_field = "unidad"

class RegistrarAccesoView(APIView):
    permission_classes = [IsAuth]
    
    def post(self, request):
        modo = request.data.get("modo", "manual")
        user_id = request.data.get("user_id")
        unidad_id = request.data.get("unidad")
        file_obj = request.FILES.get("foto")

        evidencia_key = None
        if modo in ["face", "placas"] and file_obj:
            import uuid, os
            from core.services import upload_file

            key = f"accesos/{unidad_id}/{uuid.uuid4()}.jpg"
            tmp_path = f"/tmp/{uuid.uuid4()}.jpg"

            with open(tmp_path, "wb+") as dest:
                for chunk in file_obj.chunks():
                    dest.write(chunk)

            upload_file(tmp_path, key)
            os.remove(tmp_path)

            evidencia_key = key

        acceso = Acceso.objects.create(
            user_id=user_id,
            unidad_id=unidad_id,
            modo=modo,
            tipo="residente" if user_id else "visita",
            match=True if modo != "manual" else False,
            permitido=True,
            evidencia_s3=evidencia_key
        )

        return Response({"message": "Acceso registrado", "id": acceso.pk})