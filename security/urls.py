from django.urls import path, include
from core.routers import router
from .views import VisitaViewSet, AccesoViewSet, IncidenteViewSet, AccesoEvidenciaViewSet 

router.register(r"visitas", VisitaViewSet, basename="visita")
router.register(r"accesos", AccesoViewSet, basename="acceso")
router.register(r"incidentes", IncidenteViewSet, basename="incidente")
router.register(r"accesos-evidencias", AccesoEvidenciaViewSet, basename="accesos-evidencias")

urlpatterns = [
    path("", include(router.urls)),
]