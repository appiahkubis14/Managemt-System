from django.db import models
# from inventory.models import InventoryItem

# Create your models here.

# Warehouse Management
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    # inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.inventory_item} in {self.warehouse}"

# Terminal Services Management
class TerminalActivity(models.Model):
    activity_type = models.CharField(max_length=50, choices=[("gate_in", "Gate In"), ("gate_out", "Gate Out")])
    container_id = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return f"{self.container_id} - {self.activity_type}"

# Freight Forwarding
class ShippingInstruction(models.Model):
    reference_number = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[("open", "Open"), ("closed", "Closed")])
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.reference_number
