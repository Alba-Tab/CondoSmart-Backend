from django.urls import path, include
from core.routers import router
from .views import ServicioViewSet, TicketMantenimientoViewSet

router.register(r"servicios", ServicioViewSet, basename="servicio")
router.register(r"tickets", TicketMantenimientoViewSet, basename="ticket-mantenimiento")

urlpatterns = [path("", include(router.urls))]