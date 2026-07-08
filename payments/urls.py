from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("transfer/", views.transfer_points, name="transfer"),
    path("history/", views.transfer_history, name="history"),
]