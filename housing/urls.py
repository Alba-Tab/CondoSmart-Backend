from django.urls import path, include
from core.routers import router
from .views import UnidadViewSet, ResidencyViewSet, VehiculoViewSet, MascotaViewSet, ContratoViewSet, CondominioViewSet

router.register(r"condominios", CondominioViewSet, basename="condominio")
router.register(r"unidades", UnidadViewSet, basename="unidad")
router.register(r"residencias", ResidencyViewSet, basename="residency")
router.register(r"vehiculos", VehiculoViewSet, basename="vehiculo")
router.register(r"mascotas", MascotaViewSet, basename="mascota")
router.register(r"contratos", ContratoViewSet, basename="contrato")

urlpatterns = [path("", include(router.urls))]