from django.db import models
from transport.models import Vehicle
from warehouse.models import Warehouse

# Define categories for inventory items
class ItemCategory(models.TextChoices):
    VEHICLE = "Vehicle", "Vehicle"
    FUEL = "Fuel", "Fuel"
    LUBRICANT = "Lubricant", "Lubricant"
    MACHINERY = "Machinery", "Machinery"
    OFFICE_EQUIPMENT = "Office Equipment", "Office Equipment"
    STATIONERY = "Stationery", "Stationery"

# Main Inventory Item Model
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=ItemCategory.choices, default=ItemCategory.VEHICLE)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


# Fuel Model
class Fuel(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="fuels")
    fuel_type = models.CharField(max_length=50, choices=[("Diesel", "Diesel"), ("Petrol", "Petrol")])
    storage_capacity = models.FloatField(help_text="Capacity in liters")

    def __str__(self):
        return f"{self.fuel_type} ({self.storage_capacity} L)"

# Lubricant Model
class Lubricant(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="lubricants")
    viscosity_grade = models.CharField(max_length=50)
    application_area = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.viscosity_grade} - {self.application_area}"

# Machinery Model
class Machinery(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="machinery")
    machine_type = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.machine_type} - {self.model_number}"

# Office Equipment Model
class OfficeEquipment(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="office_equipments")
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.brand} - {self.model_number}"

# Stationery Model
class Stationery(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="stationery_items")
    brand = models.CharField(max_length=100)
    paper_size = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.brand} - {self.paper_size if self.paper_size else 'N/A'}"

# Transactions Model for Inventory Usage
class InventoryTransaction(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True)
    Warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=True, null=True)
    quantity_used = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} used for {self.vehicle.license_plate if self.vehicle else 'General Use'}"
