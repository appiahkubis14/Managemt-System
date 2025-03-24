
from django.db import models

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('maintenance', 'In Maintenance'), ('in_use', 'In Use')])
    mileage = models.FloatField()
    fuel_consumption = models.FloatField()
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class Driver(models.Model):
    name = models.CharField(max_length=100)
    ghanacard_number = models.CharField(max_length=50, unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField(max_length=50)
    phone = models.CharField(max_length=10)
    phone_2 = models.CharField(max_length=10,null=True)
   
    
    def __str__(self):
        return self.name
    
class DriverAssistant(models.Model):
    name = models.CharField(max_length=100)
    ghanacard_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=10)
    phone_2 = models.CharField(max_length=10,null=True)
    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name    

class DrivervehicleAssignment(models.Model):
    driver_foreignkey = models.ForeignKey(Driver,on_delete=models.CASCADE)
    assigned_vehicle = models.OneToOneField(Vehicle,on_delete=models.SET_NULL,null=True, blank=True)
    
class AssistantdrivervehicleAssignment(models.Model):
    driver_foreignkey = models.ForeignKey(DriverAssistant,on_delete=models.CASCADE)
    assigned_vehicle = models.OneToOneField(Vehicle,on_delete=models.SET_NULL,null=True, blank=True)
    


class MaintenanceRequest(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    requested_by = models.CharField(max_length=100)
    category = models.TextField(choices=[('general', 'General'), ('accident', 'Accident'), ], default='general')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance for {self.vehicle.license_plate} - {self.status}"

class DispatchRequest(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    assistant = models.ForeignKey(DriverAssistant, on_delete=models.SET_NULL, null=True, blank=True)
    destination = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('dispatched', 'Dispatched'), ('completed', 'Completed')], default='pending')
    trip_log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispatch {self.id} - {self.status}"

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class InventoryTransaction(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True)
    quantity_used = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} used for {self.vehicle.license_plate}"

