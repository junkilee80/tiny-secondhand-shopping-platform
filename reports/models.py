from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Report(models.Model):
    TARGET_TYPE_CHOICES = [
        ("product", "상품"),
        ("user", "사용자"),
    ]

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports_made"
    )
    target_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES)
    target_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports"
    )
    target_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports_received"
    )
    reason = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter.username} reported {self.target_type}"