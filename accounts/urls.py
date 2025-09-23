from django.urls import path, include
from core.routers import router
from .views import UserViewSet, RolViewSet, MeView
router.register(r"users", UserViewSet, basename="user")
router.register(r"roles", RolViewSet, basename="rol")

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]