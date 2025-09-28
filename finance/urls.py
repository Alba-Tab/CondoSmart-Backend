from django.urls import path, include
from core.routers import router
from .views import CargoViewSet, PagoViewSet, PagoCargoViewSet
router.register(r"cargos", CargoViewSet, basename="cargo")
router.register(r"pagos", PagoViewSet, basename="pago")
router.register(r"pagocargo", PagoCargoViewSet, basename="pagocargo")
urlpatterns = [path("", include(router.urls))]