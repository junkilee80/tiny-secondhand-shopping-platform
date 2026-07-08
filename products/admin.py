from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "seller",
        "price",
        "is_blocked",
        "created_at",
    )
    list_filter = ("is_blocked", "created_at")
    search_fields = ("title", "description", "seller__username")
    list_editable = ("is_blocked",)
