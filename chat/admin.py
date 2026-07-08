from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "receiver",
        "product",
        "is_global",
        "created_at",
    )
    list_filter = ("is_global", "created_at")
    search_fields = (
        "sender__username",
        "receiver__username",
        "product__title",
        "content",
    )
