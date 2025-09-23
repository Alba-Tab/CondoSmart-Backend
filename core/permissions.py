from rest_framework.permissions import BasePermission

class IsAuth(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    
class IsResident(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(group_name='resident').exists()