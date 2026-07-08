from django.contrib import admin

from .models import Transfer


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "receiver",
        "amount",
        "memo",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "sender__username",
        "receiver__username",
        "memo",
    )
