
from django.db import models
from utils import IDGenerator, get_object_choices, vehicleTypes, vehicleDocuments, jobStatus, units, status,genderType

from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.timezone import now


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=128)
    vehicle_type = models.CharField(max_length=64)
    make = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('maintenance', 'In Maintenance'), ('in_use', 'In Use')])
    mfg_year_month = models.DateField(blank=True, null=True)
    date_of_registration = models.DateField(blank=True, null=True)
    vehicle_image = models.FileField(upload_to="uploads/images/vehicle/")
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class Driver(models.Model):
    name = models.CharField(max_length=100)
    ghanacard_number = models.CharField(max_length=50, unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField()
    phone = models.CharField(max_length=10)
    phone_2 = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_join = models.DateField(blank=True)
    gender = models.CharField(max_length=128, choices=[('male', 'Male'), ('female', 'Female')])
    photo = models.FileField(upload_to="uploads/images/drivers/")

    def __str__(self):
        return self.name


class DriverAssistant(models.Model):
    name = models.CharField(max_length=100)
    ghanacard_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=10)
    phone_2 = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_join = models.DateField(blank=True)
    gender = models.CharField(max_length=128, choices=[('male', 'Male'), ('female', 'Female')])
    photo = models.FileField(upload_to="uploads/images/assistants/")

    def __str__(self):
        return self.name


class DriverVehicleAssignment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,null=True, blank=True)
    assigned_vehicle = models.OneToOneField(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_assistant = models.OneToOneField(DriverAssistant, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.driver.name} -> {self.assigned_vehicle.license_plate}"


class AssistantDriverVehicleAssignment(models.Model):
    driver_assistant = models.ForeignKey(DriverAssistant, on_delete=models.CASCADE,null=True, blank=True)
    assigned_vehicle = models.OneToOneField(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.driver_assistant.name} -> {self.assigned_vehicle.license_plate}"


class VehicleAssignmentHistory(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    driver_assistant = models.ForeignKey(DriverAssistant, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"History: {self.vehicle.license_plate} - {self.driver.name if self.driver else 'No Driver'}"


@receiver(pre_save, sender=DriverVehicleAssignment)
def handle_driver_assignment(sender, instance, **kwargs):
    """ Automatically save previous driver assignment to history before updating. """
    old_assignment = DriverVehicleAssignment.objects.filter(assigned_vehicle=instance.assigned_vehicle).first()
    
    if old_assignment and old_assignment.driver != instance.driver:
        # Move to history before updating the new assignment
        VehicleAssignmentHistory.objects.create(
            vehicle=old_assignment.assigned_vehicle,
            driver=old_assignment.driver,
            start_date=old_assignment.assigned_date,
            end_date=now()
        )
        old_assignment.delete()  # Remove old assignment


@receiver(pre_save, sender=AssistantDriverVehicleAssignment)
def handle_assistant_assignment(sender, instance, **kwargs):
    """ Automatically save previous assistant assignment to history before updating. """
    old_assignment = AssistantDriverVehicleAssignment.objects.filter(assigned_vehicle=instance.assigned_vehicle).first()
    
    if old_assignment and old_assignment.driver_assistant != instance.driver_assistant:
        # Move to history before updating the new assignment
        VehicleAssignmentHistory.objects.create(
            vehicle=old_assignment.assigned_vehicle,
            assistant_driver=old_assignment.driver_assistant,
            start_date=old_assignment.assigned_date,
            end_date=now()
        )
        old_assignment.delete()  # Remove old assignment


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
