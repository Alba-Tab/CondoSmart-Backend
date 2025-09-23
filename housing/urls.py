from django.urls import path, include
from core.routers import router
from .views import UnidadViewSet, ResidencyViewSet

router.register(r"unidades", UnidadViewSet, basename="unidad")
router.register(r"residencias", ResidencyViewSet, basename="residency")

urlpatterns = [path("", include(router.urls))]