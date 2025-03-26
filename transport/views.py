from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import csv
import requests
from django.views.decorators.csrf import csrf_exempt

from utils import sidebar
from .models import Vehicle, DriverVehicleAssignment,\
VehicleAssignmentHistory, Driver, DriverAssistant\
, DispatchRequest,MaintenanceRequest

from .serializers import VehicleSerializer
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.db.models import Q
# from .models import DispatchRequest, DriverVehicleAssignment, Vehicle, Driver, DriverAssistant
from django.shortcuts import render, get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver


# 🚗 Transport Dashboard View
def transport_view(request):
    
    context = {
        "path": request.path or "",  # Ensure path is always a string
        "sidebar_items": sidebar.Sidebar.sidebar_items
    }
    return render(request, "transport/dashboard.html", context)


# 🚘 Vehicle Management View
def vehicle_view(request):
    vehicles = Vehicle.objects.all()  
    assignment = VehicleAssignmentHistory.objects.all()
    print(assignment.values())
    context = {
        "path": request.path or "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "vehicles": vehicles,
        "assignment": assignment
    }
    return render(request, "transport/vehicles.html", context)


# 🚀 API Endpoints for CRUD Operations
@api_view(['GET'])
def vehicle_list(request):
    """List all vehicles"""
    vehicles = Vehicle.objects.all()
    serializer = VehicleSerializer(vehicles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def vehicle_create(request):
    """Create a new vehicle"""
    serializer = VehicleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def vehicle_detail(request, id):
    """Retrieve a specific vehicle"""
    vehicle = get_object_or_404(Vehicle, id=id)
    serializer = VehicleSerializer(vehicle)
    return Response(serializer.data)


def vehicle_update(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    
    if request.method == "POST":
        if request.POST.get("_method") == "PUT":  # Simulating PUT
            form = VehicleForm(request.POST, instance=vehicle)
            if form.is_valid():
                form.save()
                return redirect("vehicle_list")  # Redirect after successful update
        else:
            return HttpResponseBadRequest("Invalid Request")

    form = VehicleForm(instance=vehicle)
    return render(request, "edit_vehicle.html", {"form": form})


@csrf_exempt  # Remove if using CSRF tokens in JS
@require_http_methods(["DELETE"])  # Only allow DELETE requests
def vehicle_delete(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    vehicle.delete()
    return JsonResponse({"message": "Vehicle deleted successfully."}, status=200)

# 📤 Export Vehicles to CSV
def export_vehicles_csv(request):
    """Exports all vehicles as a CSV file."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vehicles.csv"'

    writer = csv.writer(response)
    writer.writerow(["License Plate", "Vehicle Type", "Make", "Model", "Year", "Status", "Manufacture Date", "Date of Registration"])

    vehicles = Vehicle.objects.all()
    for vehicle in vehicles:
        writer.writerow([
            vehicle.license_plate, 
            vehicle.vehicle_type, 
            vehicle.make, 
            vehicle.model, 
            vehicle.year, 
            vehicle.status, 
            vehicle.mfg_year_month, 
            vehicle.date_of_registration
        ])

    return response

def import_vehicles(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "File is not in CSV format.")
            return redirect('dashboard_transport')

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                Vehicle.objects.create(
                    license_plate=row['License Plate'],
                    vehicle_type=row['Type'],
                    make=row['Make'],
                    model=row['Model'],
                    year=row['Year'],
                    status=row['Status'],
                    date_of_registration=row['Registered Date']
                )

            messages.success(request, "Vehicles imported successfully.")
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")
            
    return redirect('dashboard_transport')




def maintenance_request(request):
    """
    View to handle maintenance requests and update vehicle status automatically.
    """
    maintenance_requests = MaintenanceRequest.objects.all()
    vehicles = Vehicle.objects.all()
    context = {
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "maintenance_requests": maintenance_requests,
        "vehicles": vehicles,
    }

    return render(request, "transport/maintenance-request.html", context)




@receiver(post_save, sender=MaintenanceRequest)
def update_vehicle_status(sender, instance, **kwargs):
    """
    Signal to update the vehicle status based on the maintenance request status.
    """
    vehicle = instance.vehicle

    if instance.status == "approved":
        vehicle.status = "maintenance"  # Vehicle goes under maintenance
    elif instance.status == "completed":
        vehicle.status = "available"  # Vehicle is back in service
    else:
        vehicle.status = "In Use"

    vehicle.save()


def update_driver_vehicle_assignment():
    """
    Auto-populates DriverVehicleAssignment from DispatchRequest
    and ensures no vehicles in maintenance are assigned.
    """
    # from .models import DispatchRequest  # Import here to avoid circular imports

    dispatch_requests = DispatchRequest.objects.filter(status="approved")

    for dispatch in dispatch_requests:
        # Ensure vehicle is not under maintenance before assigning
        if dispatch.vehicle.status != "maintenance":
            assignment, created = DriverVehicleAssignment.objects.get_or_create(driver=dispatch.driver)

            assignment.assigned_vehicle = dispatch.vehicle
            assignment.assigned_assistant = dispatch.assistant
            assignment.save()


def driver_assistant_assignment(request):
    """
    View to handle driver-vehicle assignments, ensuring maintenance vehicles are not assigned.
    """
    update_driver_vehicle_assignment()

    assignments = DriverVehicleAssignment.objects.select_related("driver", "assigned_vehicle", "assigned_assistant").all()
    drivers = Driver.objects.all()
    vehicles = Vehicle.objects.filter(status="available")  # Exclude vehicles under maintenance
    assistants = DriverAssistant.objects.all()

    context = {
        "path": request.path or "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "assignments": assignments,
        "drivers": drivers,
        "vehicles": vehicles,
        "assistants": assistants
    }

    return render(request, "transport/driver_assistant_assignment.html", context)

def delivery_schedule(request):
    """
    View to display the delivery schedule
    """
    # Ensure assignments are up-to-date
    update_driver_vehicle_assignment()

    delivery_schedule = DispatchRequest.objects.all()
    vehicles = Vehicle.objects.all()
    drivers = Driver.objects.all()
    assistants = DriverAssistant.objects.all()
    assignments = DriverVehicleAssignment.objects.select_related("driver", "assigned_vehicle", "assigned_assistant").all()

    context = {
        "path": request.path or "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "delivery_schedule": delivery_schedule,
        "drivers": drivers,
        "vehicles": vehicles,
        "assistants": assistants
    }
    return render(request, "transport/delivery_schedule.html", context)


