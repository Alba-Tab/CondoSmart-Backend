from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.conf import settings
from .utils import get_client_ip
from core import DefaultPagination, IsAuth

# Create your views here.
class HealthView(APIView):
    
    permission_classes = [AllowAny]
    authentication_classes = [] 
    
    def get(self, request):
        return Response({
            "status": "ok",
            "service": "condosmart",
            "version": getattr(settings, "API_VERSION", "v1"),
            "ip": get_client_ip(request),
        })
        
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuth]
    pagination_class = DefaultPagination
    ordering_fields = "__all__" 
    ordering = ['id']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, is_active=True)

    def perform_update(self, serializer):
        is_active = serializer.validated_data.get("is_active", serializer.instance.is_active)
        serializer.save(updated_by=self.request.user, is_active=is_active)

        set_active = getattr(serializer.instance, "set_active", None)
        if callable(set_active):
            set_active(is_active, user=self.request.user)