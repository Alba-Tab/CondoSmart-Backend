from django.urls import path, include
from core.routers import router
from .views import UserViewSet, MeView, ChangePasswordView
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]