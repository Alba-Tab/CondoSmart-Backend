from core.views import BaseViewSet

        
class AlcanceViewSetMixin(BaseViewSet):
    """
    Filtra querysets a las unidades donde el usuario tiene derecho de acceso.
    - superuser / staff -> ven todo
    - Copropietario (Unidad.user == request.user) -> acceso permanente
    - Residente activo (Residency con status='activa') -> acceso temporal
    """
    scope_field = "unidad"

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_superuser or self.request.user.is_staff:
            return qs

        # Unidades como copropietario
        unidades_propietario = self.request.user.duenno.values_list("id", flat=True)

        # Unidades con residencia activa
        unidades_residente = self.request.user.residencias.filter(status="activa").values_list("unidad_id", flat=True)

        user_unidades = list(unidades_propietario) + list(unidades_residente)

        if not user_unidades:
            return qs.none()

        return qs.filter(**{f"{self.scope_field}__in": user_unidades})
