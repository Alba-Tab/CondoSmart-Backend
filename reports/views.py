from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from core.permissions import IsAuth
from accounts.models import CustomUser
from finance.models import Cargo, Pago, PagoCargo
from django.contrib.auth.models import Group
from communication.models import Comunicado, Notificacion
from housing.models import Unidad, Residency, Vehiculo, Mascota, Contrato

class UserReportView(APIView):
    permission_classes = [IsAuth]

    def get(self, request):
        tipo = request.query_params.get("tipo", "status")
        limit = int(request.query_params.get("limit", 20))

        if tipo == "status":
            data = CustomUser.objects.values("is_active").annotate(total=Count("id"))
        elif tipo == "group":
            data = Group.objects.annotate(total=Count("user")).values("name", "total")
        elif tipo == "audit":
            qs = CustomUser.objects.select_related("created_by", "updated_by").order_by("-created_at")[:limit]
            data = [
                {
                    "username": u.username,
                    "is_active": u.is_active,
                    "created_at": u.created_at,
                    "created_by": u.created_by.username if u.created_by else None,
                    "updated_at": u.updated_at,
                    "updated_by": u.updated_by.username if u.updated_by else None,
                }
                for u in qs
            ]
        else:
            return Response({"detail": "tipo inválido"}, status=400)

        return Response(data)

class CommunicationReportView(APIView):
    permission_classes = [IsAuth]

    def get(self, request):
        tipo = request.query_params.get("tipo")

        if tipo == "comunicado_detalle":
            comunicado_id = request.query_params.get("comunicado_id")
            if not comunicado_id:
                return Response({"detail": "Debe enviar comunicado_id"}, status=400)

            # Notificaciones vinculadas a ese comunicado
            qs = Notificacion.objects.filter(comunicado_id=comunicado_id).select_related("user")

            leidas = qs.filter(leido_at__isnull=False).values_list("user__username", flat=True)
            no_leidas = qs.filter(leido_at__isnull=True).values_list("user__username", flat=True)

            return Response({
                "comunicado_id": comunicado_id,
                "total": qs.count(),
                "leidas": list(leidas),
                "no_leidas": list(no_leidas),
            })

        return Response({"detail": "tipo inválido"}, status=400)
 
class FinanceReportView(APIView):
    permission_classes = [IsAuth]

    def get(self, request):
        tipo = request.query_params.get("tipo")

        if tipo == "total_pagado":
            total = Pago.objects.filter(estado="confirmado").aggregate(suma=Sum("monto_total"))["suma"] or 0
            return Response({"total_pagado": total})

        elif tipo == "cargos_por_estado":
            data = (
                Cargo.objects.values("estado")
                .annotate(total=Count("id"), suma=Sum("monto"))
                .order_by("estado")
            )
            return Response(data)

        elif tipo == "cargos_por_tipo":
            data = (
                Cargo.objects.values("concepto")
                .annotate(total=Count("id"), suma=Sum("monto"))
                .order_by("concepto")
            )
            return Response(data)

        elif tipo == "cargos_no_pagados":
            data = (
                Cargo.objects.filter(estado__in=["pendiente", "parcial"])
                .values("id", "unidad__code", "concepto", "descripcion", "monto", "saldo", "estado")
                .order_by("unidad__code")
            )
            return Response(list(data))

        elif tipo == "pagos_por_metodo":
            data = (
                Pago.objects.filter(estado="confirmado")
                .values("metodo")
                .annotate(total=Count("id"), suma=Sum("monto_total"))
                .order_by("metodo")
            )
            return Response(data)

        return Response({"detail": "tipo inválido"}, status=400)

from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsAuth
from housing.models import Unidad, Residency, Vehiculo, Mascota, Contrato

class HousingReportView(APIView):
    permission_classes = [IsAuth]

    def get(self, request):
        tipo = request.query_params.get("tipo")

        # Lista de todas las unidades
        if tipo == "unidades":
            data = Unidad.objects.select_related("user").values(
                "id", "code", "is_active",
                "user__id", "user__username"
            )
            return Response(list(data))

        # Lista de residencias activas
        elif tipo == "residencias_activas":
            data = Residency.objects.filter(status="activa").select_related("user","unidad").values(
                "id", "unidad__code", "user__id", "user__username",
                "tipo_ocupacion", "is_owner", "start", "end"
            )
            return Response(list(data))

        # Lista de vehículos
        elif tipo == "vehiculos":
            data = Vehiculo.objects.select_related("unidad","responsable").values(
                "id", "placa", "marca", "color",
                "unidad__code",
                "responsable__id", "responsable__username"
            )
            return Response(list(data))

        # Lista de mascotas activas
        elif tipo == "mascotas":
            data = Mascota.objects.filter(is_active=True).select_related("unidad","responsable").values(
                "id", "name", "tipo", "raza",
                "unidad__code",
                "responsable__id", "responsable__username"
            )
            return Response(list(data))

        # Lista de contratos activos
        elif tipo == "contratos_activos":
            data = Contrato.objects.filter(is_active=True).select_related("unidad","duenno","inquilino").values(
                "id", "unidad__code", "descripcion",
                "duenno__id", "duenno__username",
                "inquilino__id", "inquilino__username",
                "start", "end", "monto_mensual"
            )
            return Response(list(data))

        return Response({"detail": "tipo inválido"}, status=400)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    