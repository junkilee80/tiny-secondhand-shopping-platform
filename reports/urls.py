from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("product/<int:product_id>/", views.report_product, name="product"),
    path("user/<int:user_id>/", views.report_user, name="user"),
]