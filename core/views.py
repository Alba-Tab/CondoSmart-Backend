from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.conf import settings
from .utils import get_client_ip


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
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
        
    #def perform_destroy(self, instance):
    #    instance.delete(user=self.request.user)