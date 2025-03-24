from django.contrib import admin
from .models import Vehicle, Driver, DriverAssistant, DriverVehicleAssignment, AssistantDriverVehicleAssignment, VehicleAssignmentHistory, MaintenanceRequest, DispatchRequest, InventoryItem, InventoryTransaction


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vehicle_type', 'make', 'model', 'year', 'status')
    search_fields = ('license_plate', 'make', 'model')
    list_filter = ('status',)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'ghanacard_number', 'license_number', 'phone', 'gender')
    search_fields = ('name', 'ghanacard_number', 'license_number')
    list_filter = ('gender',)


@admin.register(DriverAssistant)
class DriverAssistantAdmin(admin.ModelAdmin):
    list_display = ('name', 'ghanacard_number', 'phone', 'gender')
    search_fields = ('name', 'ghanacard_number')
    list_filter = ('gender',)


@admin.register(DriverVehicleAssignment)
class DriverVehicleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('driver', 'assigned_vehicle', 'assigned_date')
    search_fields = ('driver__name', 'assigned_vehicle__license_plate')
    list_filter = ('assigned_date',)
    ordering = ('-assigned_date',)  # Using the correct field


@admin.register(AssistantDriverVehicleAssignment)
class AssistantDriverVehicleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('driver_assistant', 'assigned_vehicle', 'assigned_date')
    search_fields = ('driver_assistant__name', 'assigned_vehicle__license_plate')
    list_filter = ('assigned_date',)
    ordering = ('-assigned_date',)  # Using the correct field


@admin.register(VehicleAssignmentHistory)
class VehicleAssignmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'driver', 'driver_assistant', 'start_date', 'end_date')
    search_fields = ('vehicle__license_plate', 'driver__name', 'driver_assistant__name')
    list_filter = ('start_date', 'end_date')


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'requested_by', 'category', 'status', 'created_at')
    search_fields = ('vehicle__license_plate', 'requested_by')
    list_filter = ('status', 'category', 'created_at')


@admin.register(DispatchRequest)
class DispatchRequestAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'driver', 'assistant', 'destination', 'status', 'created_at')
    search_fields = ('vehicle__license_plate', 'driver__name', 'assistant__name', 'destination')
    list_filter = ('status', 'created_at')


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'reorder_level')
    search_fields = ('name',)


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('item', 'vehicle', 'quantity_used', 'transaction_date')
    search_fields = ('item__name', 'vehicle__license_plate')
    list_filter = ('transaction_date',)

