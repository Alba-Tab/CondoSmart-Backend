from django.urls import path, include
from core.routers import router
from .views import AreaComunViewSet, ReservaViewSet, SuministroViewSet

router.register(r"areas", AreaComunViewSet, basename="area")
router.register(r"suministros", SuministroViewSet, basename="suministro")
router.register(r"reservas", ReservaViewSet, basename="reserva")

urlpatterns = [path("", include(router.urls))]
