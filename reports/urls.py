from django.urls import path
from .views import UserReportView, CommunicationReportView, FinanceReportView, HousingReportView

urlpatterns = [
    path("users/report/", UserReportView.as_view(), name="user_report"),
    path("communication/", CommunicationReportView.as_view(), name="communication_report"),
    path("finance/", FinanceReportView.as_view(), name="finance_report"),
    path("housing/", HousingReportView.as_view(), name="housing_report"),
]

