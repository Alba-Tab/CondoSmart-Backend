from django.urls import path, include
from core.routers import router
from .views import UserViewSet, RolViewSet, PasswordChangeView
router.register(r"users", UserViewSet, basename="user")
router.register(r"roles", RolViewSet, basename="rol")

urlpatterns = [path("", include(router.urls)), 
               path("password-change/", PasswordChangeView.as_view(), name="password-change")]