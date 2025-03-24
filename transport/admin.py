from django.contrib import admin
from .models import (
    Vehicle, Driver, DriverAssistant, DrivervehicleAssignment, 
    AssistantdrivervehicleAssignment, MaintenanceRequest, 
    DispatchRequest, InventoryItem, InventoryTransaction
)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'make', 'model', 'year', 'status', 'mileage', 'fuel_consumption')
    list_filter = ('status', 'vehicle_type', 'year')
    search_fields = ('license_plate', 'make', 'model')
    ordering = ('year',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'ghanacard_number', 'license_number', 'license_expiry_date', 'phone', 'gender')
    search_fields = ('name', 'ghanacard_number', 'license_number')
    list_filter = ('gender',)
    ordering = ('name',)

@admin.register(DriverAssistant)
class DriverAssistantAdmin(admin.ModelAdmin):
    list_display = ('name', 'ghanacard_number', 'phone', 'gender', 'assigned_vehicle')
    search_fields = ('name', 'ghanacard_number')
    list_filter = ('gender',)
    ordering = ('name',)

@admin.register(DrivervehicleAssignment)
class DrivervehicleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('driver_foreignkey', 'assigned_vehicle')
    search_fields = ('driver_foreignkey__name', 'assigned_vehicle__license_plate')

@admin.register(AssistantdrivervehicleAssignment)
class AssistantdrivervehicleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('driver_foreignkey', 'assigned_vehicle')
    search_fields = ('driver_foreignkey__name', 'assigned_vehicle__license_plate')

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'requested_by', 'category', 'status', 'created_at')
    search_fields = ('vehicle__license_plate', 'requested_by')
    list_filter = ('status', 'category')
    ordering = ('-created_at',)

@admin.register(DispatchRequest)
class DispatchRequestAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'driver', 'assistant', 'destination', 'status', 'created_at')
    search_fields = ('vehicle__license_plate', 'driver__name', 'destination')
    list_filter = ('status',)
    ordering = ('-created_at',)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'reorder_level')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('item', 'vehicle', 'quantity_used', 'transaction_date')
    search_fields = ('item__name', 'vehicle__license_plate')
    ordering = ('-transaction_date',)
