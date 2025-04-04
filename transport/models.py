
from django.db import models
from utils import IDGenerator, get_object_choices, vehicleTypes, vehicleDocuments, jobStatus, units, status,genderType

from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.timezone import now
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



class VehicleType(models.TextChoices):
    TRUCK = "Truck", "Truck"
    TRAILER = "Trailer", "Trailer"
    PICKUP = "Pickup", "Pickup"
    MOTORCYCLE = "Motorcycle", "Motorcycle"
    VAN = "Van", "Van"
    BUS = "Bus", "Bus"
    FORKLIFT = "Forklift", "Forklift"
    TANKER = "Tanker", "Tanker"
    SUV = "SUV", "SUV"
    SEDAN = "Sedan", "Sedan"
    HATCHBACK = "Hatchback", "Hatchback"
    MINIBUS = "Minibus", "Minibus"
    DUMP_TRUCK = "Dump Truck", "Dump Truck"
    CONCRETE_MIXER = "Concrete Mixer", "Concrete Mixer"
    CONTAINER_CARRIER = "Container Carrier", "Container Carrier"
    TRACTOR = "Tractor", "Tractor"
    CRANE = "Crane", "Crane"
    BULLDOZER = "Bulldozer", "Bulldozer"
    EXCAVATOR = "Excavator", "Excavator"
    FLATBED_TRUCK = "Flatbed Truck", "Flatbed Truck"
    TIPPER_TRUCK = "Tipper Truck", "Tipper Truck"
    REFRIGERATED_TRUCK = "Refrigerated Truck", "Refrigerated Truck"
    AMBULANCE = "Ambulance", "Ambulance"
    FIRE_TRUCK = "Fire Truck", "Fire Truck"
    TOW_TRUCK = "Tow Truck", "Tow Truck"

class VehicleTypeDetail(models.Model):
    type = models.CharField(max_length=64, choices=VehicleType.choices)
    make = models.CharField(max_length=64)
    model = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.type} - {self.make} {self.model}"


    def __str__(self):
        return f"{self.type} - {self.make} {self.model}"

class Vehicle(models.Model):
    LICENSE_PLATE_REGEX = r'^[A-Z]{2}-\d{3,4}-\d{2}$'

    license_plate = models.CharField(
        max_length=128,
        unique=True,
        validators=[RegexValidator(
            regex=LICENSE_PLATE_REGEX,
            message="License plate must be in the format 'GH-1234-21'.",
            code='invalid_license_plate'
        )]
    )
    vehicle_type = models.ForeignKey(VehicleTypeDetail,on_delete=models.CASCADE , related_name="specific_vehicle_details")
    make = models.CharField(max_length=128,blank=True, null=True)
    model = models.CharField(max_length=128,blank=True, null=True)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('maintenance', 'Maintenance'), ('out_of_service', 'Out of Service'), ('retired', 'Retired'), ('scrapped', 'Scrapped'), ('damaged', 'Damaged'), ('stolen', 'Stolen'), ('lost', 'Lost'), ('unknown', 'Unknown')], default='active')
    # fuel_type = models.CharField(max_length=50, choices=[('petrol', 'Petrol'), ('diesel', 'Diesel'), ('electric', 'Electric')], null=True, blank=True)
    mfg_year_month = models.DateField(blank=True, null=True)
    date_of_registration = models.DateField(blank=True, null=True)
    vehicle_image = models.FileField(upload_to="uploads/images/vehicle/")
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class ClientRequestDetail(models.Model):
    REQUEST_TYPES = [
        ('TRANSPORT', 'Freight Transport'),
        ('EXPRESS', 'Express Delivery'),
        ('BULK', 'Bulk Cargo Shipping'),
        ('COLD_CHAIN', 'Cold Chain Logistics'),
        ('HAZARD', 'Hazardous Material Transport'),
        ('LAST_MILE', 'Last-Mile Delivery'),
        ('RETURN', 'Return Logistics'),
        ('DEDICATED', 'Dedicated Vehicle Service'),
        ('VEHICLE_RENTAL', 'Short-Term Vehicle Rental'),
        ('LEASING', 'Long-Term Leasing'),
        ('TRACKING', 'Real-Time GPS Tracking'),
        ('MAINTENANCE', 'Regular Vehicle Maintenance'),
        ('REPAIR', 'Emergency Breakdown Assistance'),
        ('DOCUMENTATION', 'Customs & Documentation'),
        ('SECURITY', 'Escort Vehicle Service'),
        ('INSURANCE', 'Insurance Coverage'),
        ('PAYMENT', 'Invoice & Billing Requests'),
    ]

    client_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPES)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE , related_name='client_requested_vehicle')
    description = models.TextField(blank=True, null=True)
    pickup_location = models.CharField(max_length=255, blank=True, null=True)
    delivery_location = models.CharField(max_length=255, blank=True, null=True)
    scheduled_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled'),
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.username} - {self.get_request_type_display()} - {self.status}"


class Driver(models.Model):
    name = models.CharField(max_length=100)
    ghanacard_number = models.CharField(max_length=50, unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField()
    phone = models.CharField(max_length=10)
    phone_2 = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_join = models.DateField(default=now ,blank=True,null=True)
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
    date_of_join = models.DateField(default=now , blank=True,null=True)
    gender = models.CharField(max_length=128, choices=[('male', 'Male'), ('female', 'Female')])
    photo = models.FileField(upload_to="uploads/images/assistants/")

    def __str__(self):
        return self.name


class DriverVehicleAssignment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,null=True, blank=True)
    assigned_vehicle = models.OneToOneField(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.driver.name} -> {self.assigned_vehicle.license_plate}"

class AssistantDriverVehicleAssignment(models.Model):
    driver_assistant = models.ForeignKey(DriverAssistant, on_delete=models.CASCADE,null=True, blank=True)
    assigned_vehicle = models.OneToOneField(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.driver_assistant.name} -> {self.assigned_vehicle.license_plate}"


class CurrentVehicleAssignment(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name="current_assignment")
    current_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    current_assistant = models.ForeignKey(DriverAssistant, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vehicle: {self.vehicle.license_plate} | Driver: {self.current_driver} | Assistant: {self.current_assistant}"
    

# SIGNALS TO AUTOMATICALLY UPDATE CurrentVehicleAssignment
@receiver(post_save, sender=DriverVehicleAssignment)
def update_current_driver(sender, instance, **kwargs):
    if instance.assigned_vehicle:
        current_assignment, created = CurrentVehicleAssignment.objects.get_or_create(vehicle=instance.assigned_vehicle)
        current_assignment.current_driver = instance.driver
        current_assignment.save()

@receiver(post_save, sender=AssistantDriverVehicleAssignment)
def update_current_assistant(sender, instance, **kwargs):
    if instance.assigned_vehicle:
        current_assignment, created = CurrentVehicleAssignment.objects.get_or_create(vehicle=instance.assigned_vehicle)
        current_assignment.current_assistant = instance.driver_assistant
        current_assignment.save()






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





from django.db import models

class ClientRequestInfo(models.Model):
    status_choices = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    REQUEST_TYPES = [
        ('TRANSPORT', 'Transport'),
        ('DELIVERY', 'Delivery'),
        ('OTHER', 'Other'),
    ]
  
    client_name = models.CharField(max_length=255)
    email = models.EmailField()
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPES)
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING')
    description = models.TextField(blank=True, null=True)
    vehicle_license_plate = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50)
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    driver = models.CharField( null=True, blank=True)
    assistant = models.CharField(null=True, blank=True)
    pickup_location = models.CharField(max_length=255)
    delivery_location = models.CharField(max_length=255)
    trip_log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} - {self.vehicle_license_plate}"
