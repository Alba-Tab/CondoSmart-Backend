from django.urls import path, include
from core.routers import router
from .views import ServicioViewSet, TicketMantenimientoViewSet, TarifaServicioViewSet

router.register(r"servicios", ServicioViewSet, basename="servicio")
router.register(r"tickets", TicketMantenimientoViewSet, basename="ticket-mantenimiento")
router.register(r"tarifas-servicio", TarifaServicioViewSet, basename="tarifa-servicio")

urlpatterns = [path("", include(router.urls))]