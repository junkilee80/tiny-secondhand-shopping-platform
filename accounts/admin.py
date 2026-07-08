from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "points",
        "is_suspended",
    )
    list_filter = ("is_suspended",)
    search_fields = ("user__username", "user__email", "bio")