
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import ForeignKey
from accounts.models import Rol, CustomUser
from housing.models import Residency, Unidad


class IsAuth(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    
class IsResident(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(group_name='resident').exists()
