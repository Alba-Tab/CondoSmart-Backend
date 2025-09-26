from rest_framework.permissions import BasePermission

class IsAuth(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsAdmin(BasePermission):
    """Admin = cualquier usuario con is_staff."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class isResident(BasePermission):
    """Permite restringir acceso a usuarios en el grupo 'resident'."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="resident").exists()
    
class IsInGroup(BasePermission):
    """Permite restringir acceso a usuarios de un grupo específico (ej. guard, resident)."""
    required_group = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if self.required_group is None:
            return False
        return request.user.groups.filter(name=self.required_group).exists()

class AlcancePermission(BasePermission):
    """
    Da acceso a un objeto si pertenece a una unidad donde el usuario:
    - es superuser o staff (ve todo)
    - es copropietario (Unidad.user)
    - tiene residencia activa
    """
    scope_field = "unidad"

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Copropietario
        unidades_propietario = request.user.duenno.values_list("id", flat=True)

        # Residente activo
        unidades_residente = request.user.residencias.filter(status="activa").values_list("unidad_id", flat=True)

        user_unidades = list(unidades_propietario) + list(unidades_residente)

        if not user_unidades:
            return False

        objeto_unidad = getattr(obj, self.scope_field, None)
        return objeto_unidad and objeto_unidad.id in user_unidades