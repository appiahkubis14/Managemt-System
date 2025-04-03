from django import forms
from .models import DispatchRequest, DriverVehicleAssignment

class DispatchRequestForm(forms.ModelForm):
    class Meta:
        model = DispatchRequest
        fields = ['vehicle', 'driver', 'assistant', 'destination', 'status', 'trip_log']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Prepopulate fields if a DriverVehicleAssignment exists for the driver
        latest_assignment = DriverVehicleAssignment.objects.filter(driver=self.initial.get('driver')).last()

        if latest_assignment:
            self.fields['vehicle'].initial = latest_assignment.assigned_vehicle
            self.fields['driver'].initial = latest_assignment.driver
            self.fields['assistant'].initial = latest_assignment.assigned_assistant
