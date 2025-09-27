from django.db import models
from core.middleware import get_user
from rest_framework import viewsets
from core.views import BaseViewSet
class AuditSaveMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_user()
        print("DEBUG user en AuditSaveMixin:", user)
        if user and getattr(user, "is_authenticated", False):
            # Superuser y staff también son usuarios válidos
            if not getattr(self, "created_by_id", None):
                self.created_by = user
            self.updated_by = user

        super().save(*args, **kwargs)
        
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
