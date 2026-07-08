from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.global_chat, name="global"),
    path("inbox/", views.inbox, name="inbox"),
    path("product/<int:product_id>/user/<int:user_id>/", views.direct_chat, name="direct"),
]