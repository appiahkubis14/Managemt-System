from django.contrib import admin
from .models import Vehicle, Driver, DriverAssistant, DriverVehicleAssignment, \
AssistantDriverVehicleAssignment, MaintenanceRequest,\
 DispatchRequest,ClientRequestInfo,VehicleTypeDetail,CurrentVehicleAssignment
from django import forms


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["make"].widget.attrs["readonly"] = True
        self.fields["model"].widget.attrs["readonly"] = True

    class Media:
        js = ("js/vehicle_autofill.js",)  # JavaScript for frontend auto-fill

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    form = VehicleForm
    list_display = ("license_plate", "vehicle_type", "make", "model", "year", "status")

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


# @admin.register(VehicleAssignmentHistory)
# class VehicleAssignmentHistoryAdmin(admin.ModelAdmin):
#     list_display = ('vehicle', 'driver', 'driver_assistant', 'start_date', 'end_date')
#     search_fields = ('vehicle__license_plate', 'driver__name', 'driver_assistant__name')
#     list_filter = ('start_date', 'end_date')


@admin.register(CurrentVehicleAssignment)
class CurrentVehicleAssignmentAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "current_driver", "current_assistant", "updated_at")
    search_fields = ("vehicle__license_plate", "current_driver__name", "current_assistant__name")
    list_filter = ("updated_at",)


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


@admin.register(ClientRequestInfo)
class ClientRequestInfoAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'email', 'request_type','description', 'pickup_location', 'delivery_location', 'scheduled_date', 'status')
    search_fields = ('client_name',)


@admin.register(VehicleTypeDetail)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'make', 'model')
    search_fields = ('type',)
    # list_filter = ('transaction_date',)

