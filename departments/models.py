from django.db import models

class Department(models.Model):
    TRANSPORT = "Transport"
    WAREHOUSE = "Warehouse"
    PROCUREMENT_INVENTORY = "Procurement & Inventory Management"

    DEPARTMENT_CHOICES = [
        (TRANSPORT, "Handles logistics, vehicle management, and transportation of goods."),
        (WAREHOUSE, "Manages storage, inventory control, and distribution of products."),
        (PROCUREMENT_INVENTORY, "Oversees purchasing, supplier relationships, and inventory control."),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        choices=[(choice, choice) for choice, _ in DEPARTMENT_CHOICES]
    )
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Auto-fill description based on department choice."""
        if not self.description:
            self.description = dict(self.DEPARTMENT_CHOICES).get(self.name, "")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
