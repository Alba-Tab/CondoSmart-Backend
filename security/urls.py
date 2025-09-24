from django.urls import path, include
from core.routers import router
from .views import VisitaViewSet, AccesoViewSet, IncidenteViewSet

router.register(r"visitas", VisitaViewSet, basename="visita")
router.register(r"accesos", AccesoViewSet, basename="acceso")
router.register(r"incidentes", IncidenteViewSet, basename="incidente")

urlpatterns = [path("", include(router.urls))]