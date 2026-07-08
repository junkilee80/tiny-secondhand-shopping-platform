from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("new/", views.product_create, name="create"),
    path("<int:product_id>/", views.product_detail, name="detail"),
    path("<int:product_id>/edit/", views.product_update, name="update"),
    path("<int:product_id>/delete/", views.product_delete, name="delete"),
]