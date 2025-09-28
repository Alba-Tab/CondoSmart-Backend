from django.urls import path, include
from core.routers import router
from .views import AreaComunViewSet, ReservaViewSet, SuministroViewSet, ReservaSuministroViewSet

router.register(r"areas", AreaComunViewSet, basename="area")
router.register(r"suministros", SuministroViewSet, basename="suministro")
router.register(r"reservas", ReservaViewSet, basename="reserva")
router.register(r"reservasuministros", ReservaSuministroViewSet, basename="reserva-suministro")

urlpatterns = [path("", include(router.urls))]
