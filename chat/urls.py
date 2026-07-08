from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.global_chat, name="global"),
]