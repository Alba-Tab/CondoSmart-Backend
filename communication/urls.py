from django.urls import path, include
from core.routers import router
from .views import ComunicadoViewSet, NotificacionViewSet

router.register(r"comunicados", ComunicadoViewSet, basename="comunicado")
router.register(r"notificaciones", NotificacionViewSet, basename="notificacion")

urlpatterns = [path("", include(router.urls))]