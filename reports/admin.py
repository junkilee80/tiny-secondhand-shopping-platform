from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reporter",
        "target_type",
        "target_product",
        "target_user",
        "created_at",
    )
    list_filter = ("target_type", "created_at")
    search_fields = (
        "reporter__username",
        "target_user__username",
        "target_product__title",
        "reason",
    )