from django.conf import settings
from django.db import models

class DesignPackage(models.Model):
    name = models.CharField(max_length=80) 
    description = models.TextField()
    base_price_eur = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DesignOrder(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("awaiting_payment", "Awaiting Payment"),
        ("paid", "Paid"),
        ("in_progress", "In Progress"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="design_orders")
    package = models.ForeignKey(DesignPackage, on_delete=models.PROTECT, related_name="orders")

    design_type = models.CharField(max_length=60)  
    size = models.CharField(max_length=60, blank=True) 
    brief = models.TextField()  # what they want
    quoted_price_eur = models.DecimalField(max_digits=8, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.user} - {self.status}"


class Deliverable(models.Model):
    order = models.ForeignKey(DesignOrder, on_delete=models.CASCADE, related_name="deliverables")
    file = models.FileField(upload_to="deliverables/")
    note = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Deliverable for Order #{self.order_id}"
