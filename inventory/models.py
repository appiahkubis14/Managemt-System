from django.db import models
from transport.models import Vehicle
from warehouse.models import Warehouse

# Define categories for inventory items
from django.db import models
from departments.models import Department
from employees.models import Employee
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User
from .utils import ItemCategory


# Inventory Model
def get_default_department():
    return Department.objects.filter(name="Transport").first() 

class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    reorder_level = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, default=get_default_department)
    # cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    # retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    # supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    # expiration_date = models.DateField(null=True, blank=True)
    # updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_below_reorder_level(self):
        return self.quantity <= self.reorder_level

    def __str__(self):
        return f"{self.name} ({self.quantity})"
    


from django.db import models
from django.db.models import F

class UniqueInventoryItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=ItemCategory.choices)
    quantity = models.PositiveIntegerField(default=0)  # To accumulate quantities
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    reorder_level = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, default=get_default_department)
    created_at = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)  # Automatically updates to current time when saved

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    @classmethod
    def update_or_create_inventory(cls, name, category, description, unit_price, reorder_level, department, quantity):
        """Create or update an item in UniqueInventoryItem by aggregating quantities."""
        item, created = cls.objects.update_or_create(
            name=name, 
            category=category, 
            unit_price=unit_price,
            defaults={
                'quantity': F('quantity') + quantity,  # Add new quantity to existing
                'description': description,
                'reorder_level': reorder_level,
                'department': department
            }
        )
        return item, created



# Stock Receiving
class StockReceive(models.Model):
    RECEIPT_STATUS = [('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_received = models.PositiveIntegerField()
    supplier = models.CharField(max_length=255, blank=True, null=True) 
    received_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    received_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=RECEIPT_STATUS, default='PENDING')

    def save(self, *args, **kwargs):
        if self.status == "APPROVED":
            self.item.quantity += self.quantity_received
            self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Received {self.quantity_received} {self.item.name}"
    

# Stock Transactions (Issue, Return, Transfer)
class StockTransaction(models.Model):
    TRANSACTION_TYPES = [('ISSUE', 'Issue'), ('RETURN', 'Return'), ('TRANSFER', 'Transfer')]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.transaction_type == "ISSUE" and self.item.quantity >= self.quantity:
            self.item.quantity -= self.quantity
        elif self.transaction_type in ["RETURN", "TRANSFER"]:
            self.item.quantity += self.quantity
        self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} - {self.quantity} units"


class TransactionType(models.TextChoices):
    PENDING = "Pending", "Pending"
    APPROVED = "Approved", "Approved"
    REJECTED = "Rejected", "Rejected"
    ABORTED = "Aborted", "Aborted"
    ISSUED = "Issued", "Issued"
    RECEIVED = "Received", "Received"
    RETURNED = "Returned", "Returned"
    TRANSFERRED = "Transferred", "Transferred"


class InventoryRequest(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)  # Assuming category is a string
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    
    from_department = models.ForeignKey(Department, related_name="requests_out", null=True, blank=True, on_delete=models.SET_NULL)
    to_department = models.ForeignKey(Department, related_name="requests_in", null=True, blank=True, on_delete=models.SET_NULL)

    # Employee details stored separately
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    employee_name = models.CharField(max_length=255, blank=True, null=True)
    employee_gender = models.CharField(max_length=10, blank=True, null=True)
    employee_phone = models.CharField(max_length=20, blank=True, null=True)
    employee_ghana_card_number = models.CharField(max_length=50, blank=True, null=True)
    employee_position = models.CharField(max_length=100, blank=True, null=True)
    employee_photo = models.ImageField(upload_to="employee_photos/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Handles stock updates based on transaction type"""
        if self.transaction_type in [TransactionType.ISSUED, TransactionType.TRANSFERRED]:
            if self.item.quantity < self.quantity:
                raise ValidationError("Not enough stock available!")
            self.item.quantity -= self.quantity
        elif self.transaction_type in [TransactionType.RECEIVED, TransactionType.RETURNED]:
            self.item.quantity += self.quantity

        # Auto-fill employee details if an employee is assigned
        if self.employee:
            self.employee_name = self.employee_name
            self.employee_gender = self.employee.gender
            self.employee_phone = self.employee.phone
            self.employee_ghana_card_number = self.employee.ghana_card
            self.employee_position = self.employee.position
            self.employee_photo = self.employee.photo

        self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.quantity})"



class InventoryTransaction(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)  # Assuming category is a string
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    
    from_department = models.ForeignKey(Department, related_name="transactions_out", null=True, blank=True, on_delete=models.SET_NULL)
    to_department = models.ForeignKey(Department, related_name="transactions_in", null=True, blank=True, on_delete=models.SET_NULL)

    # Employee handling the request
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    employee_name = models.CharField(max_length=255, blank=True, null=True)
    employee_gender = models.CharField(max_length=10, blank=True, null=True)
    employee_phone = models.CharField(max_length=20, blank=True, null=True)
    employee_ghana_card_number = models.CharField(max_length=50, blank=True, null=True)
    employee_position = models.CharField(max_length=100, blank=True, null=True)
    employee_photo = models.ImageField(upload_to="employee_photos/", blank=True, null=True)

    # Storekeeper approval
    approved_by = models.ForeignKey(Employee, related_name="approved_transactions", on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Handles stock updates when a transaction is approved"""
        if not self.approved_by:
            raise ValidationError("Transaction must be approved by a storekeeper.")

        if self.transaction_type in [TransactionType.ISSUED, TransactionType.TRANSFERRED]:
            if self.item.quantity < self.quantity:
                raise ValidationError("Not enough stock available!")
            self.item.quantity -= self.quantity
        elif self.transaction_type in [TransactionType.RECEIVED, TransactionType.RETURNED]:
            self.item.quantity += self.quantity

        # Auto-fill employee details if an employee is assigned
        if self.employee:
            self.employee_name = self.employee.name
            self.employee_gender = self.employee.gender
            self.employee_phone = self.employee.phone
            self.employee_ghana_card_number = self.employee.ghana_card
            self.employee_position = self.employee.position
            self.employee_photo = self.employee.photo

        self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.quantity}) - Approved by {self.approved_by.name if self.approved_by else 'N/A'}"



# class InventoryIssue(models.Model):
#     inventory_request = models.ForeignKey(InventoryRequest, on_delete=models.CASCADE)
#     issue_date = models.DateTimeField(auto_now_add=True)
#     quantity_issued = models.PositiveIntegerField()
#     warehouse_location = models.CharField(max_length=100)

#     def __str__(self):
#         return f'{self.inventory_request.item.name} issued to {self.inventory_request.vehicle.license_plate}'


# class Supplier(models.Model):
#     name = models.CharField(max_length=255)
#     contact_name = models.CharField(max_length=100)
#     contact_email = models.EmailField()
#     contact_phone = models.CharField(max_length=15)
#     address = models.TextField()

#     def __str__(self):
#         return self.name


# class MaintenanceLog(models.Model):
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     maintenance_type = models.CharField(max_length=100)
#     maintenance_date = models.DateTimeField(auto_now_add=True)
#     parts_used = models.ManyToManyField(InventoryItem)
#     mileage_at_maintenance = models.PositiveIntegerField()
#     remarks = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f'Maintenance for {self.vehicle.license_plate} on {self.maintenance_date}'


# class StockMovement(models.Model):
#     MOVEMENT_TYPE = [
#         ('received', 'Received'),
#         ('transferred', 'Transferred'),
#         ('issued', 'Issued'),
#     ]
#     item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     movement_type = models.CharField(max_length=50, choices=MOVEMENT_TYPE)
#     source_location = models.CharField(max_length=100)
#     destination_location = models.CharField(max_length=100)
#     movement_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.quantity} {self.item.name} {self.movement_type}'



# class StockReplenishment(models.Model):
#     item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
#     reorder_level = models.PositiveIntegerField()
#     quantity_to_reorder = models.PositiveIntegerField()
#     date_requested = models.DateTimeField(auto_now_add=True)
#     supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
#     status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('ordered', 'Ordered'), ('delivered', 'Delivered')], default='pending')

#     def __str__(self):
#         return f'Replenishment for {self.item.name} - {self.status}'





















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