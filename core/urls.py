from django.urls import path, include
from .views import HealthView
from .routers import router

urlpatterns = [
    path("", include("accounts.urls")),
    path("", include("housing.urls")),
    path("health/", HealthView.as_view(), name="health"),
    path("", include("security.urls")),
    path("", include("reservations.urls")),
    path("", include("finance.urls")),
    path("", include("communication.urls")),
    path("", include("maintenance.urls")),
    #path("", include("reports.urls")),
    
    path("router/", include(router.urls)),  # opcional para inspección
]
