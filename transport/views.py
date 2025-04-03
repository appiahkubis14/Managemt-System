from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils.timezone import now
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View
from django.db import models
from django.db.models import Q, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import csv
import json
import requests
from datetime import datetime

from utils import sidebar
from .models import (
    Vehicle, 
    DriverVehicleAssignment, 
    Driver, 
    DriverAssistant, 
    DispatchRequest, 
    MaintenanceRequest, 
    CurrentVehicleAssignment, 
    ClientRequestDetail, 
    ClientRequestInfo
)
# from .serializers import VehicleSerializer
from inventory.models import InventoryItem, InventoryRequest, TransactionType, ItemCategory
from employees.models import Employee
from departments.models import Department





def transport_view(request):
    """
    Renders the transport dashboard.
    """
    current_assignments = CurrentVehicleAssignment.objects.all()

    for assignment in current_assignments:
        print(f"Vehicle: {assignment.vehicle.license_plate} | Driver: {assignment.current_driver} | Assistant: {assignment.current_assistant}")

    context = {
        "path": request.path or "",  # Ensure path is always a string
        "sidebar_items": sidebar.Sidebar.sidebar_items,
    }
    return render(request, "transport/dashboard.html", context)

def transport_data(request):
    """
    API endpoint to provide transport data in JSON format.
    """
    # Fetch key statistics
    total_vehicles = Vehicle.objects.count()
    total_drivers = Driver.objects.count()
    total_assignments = DriverVehicleAssignment.objects.count()

    # Aggregate data for charts
    vehicle_status = list(Vehicle.objects.values('status').annotate(count=Count('status')))
    maintenance_requests = list(MaintenanceRequest.objects.values('status').annotate(count=Count('status')))
    dispatch_requests = list(DispatchRequest.objects.values('status').annotate(count=Count('status')))

    # Top 5 most assigned vehicles
    top_vehicles = list(
        DriverVehicleAssignment.objects.values(
            'assigned_vehicle__license_plate',
            'assigned_vehicle__status',
            'assigned_vehicle__date_of_registration',
        )
        .annotate(count=Count('assigned_vehicle'))
        .order_by('-count')[:5]
    )
    # Ensure clean response format
    data = {
        "total_vehicles": total_vehicles,
        "total_drivers": total_drivers,
        "total_assignments": total_assignments,
        "vehicle_status": vehicle_status,
        "maintenance_requests": maintenance_requests,
        "dispatch_requests": dispatch_requests,
        "top_vehicles": top_vehicles,
    }
    return JsonResponse(data)

def requested_inventory(request):
    inventories = InventoryItem.objects.all()
    employees = Employee.objects.all()
    departments = Department.objects.all()

    # Get the Transport department instance
    transport_department = get_object_or_404(Department, name="Transport")

    # Filter inventory requests where to_department is Transport
    inventory_request = InventoryRequest.objects.filter(to_department=transport_department)

    context = {
        "path": request.path if request.path else "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "inventories": inventories,
        "employees": employees,
        "departments": departments,
        "inventory_request": inventory_request,
        "TransactionType": TransactionType
    }
    return render(request, "transport/requested-inventories.html", context)



def save_client_dispatch_request(request):
    if request.method == "POST":
        client_name = request.POST.get("client_name")
        email = request.POST.get("email")
        request_type = request.POST.get("request_type")
        scheduled_date = request.POST.get("scheduled_date")
        destination = request.POST.get("destination")
        status = request.POST.get("status", "pending")
        trip_log = request.POST.get("trip_log", "")

        # Save the client dispatch request to the database
        client_details = ClientRequestDetail.objects.create(
            client_name=client_name,
            email=email,
            request_type=request_type,
            scheduled_date=scheduled_date,
            destination=destination,
            status=status,
            trip_log=trip_log
        )

        license_plate = request.POST.get("license_plate")
        vehicle_type = request.POST.get("vehicle_type")
        make = request.POST.get("make")
        model = request.POST.get("model")
        vehicle = request.POST.get("vehicle")
























##########################################################################################################################
from django.shortcuts import render
from django.conf import settings

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Vehicle
import traceback

def vehicle_view(request):
    context = {
        "path": request.path or "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
    }
    return render(request, "transport/vehicles.html", context)





@csrf_exempt
def vehicle_list_api(request):
    try:
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()  # ✅ Get search query

        vehicles = Vehicle.objects.select_related("vehicle_type").all()

        # ✅ Apply search filter
        if search_value:
            vehicles = vehicles.filter(
                Q(license_plate__icontains=search_value) |
                Q(vehicle_type__type__icontains=search_value) |
                Q(make__icontains=search_value) |
                Q(model__icontains=search_value) |
                Q(status__icontains=search_value)
            )

        paginator = Paginator(vehicles, length)
        page_number = (start // length) + 1
        page = paginator.get_page(page_number)

        data = [
            {
                "id": vehicle.id,
                "license_plate": vehicle.license_plate,
                "vehicle_type": vehicle.vehicle_type.type if vehicle.vehicle_type else None,
                "make": vehicle.make,
                "model": vehicle.model,
                "year": vehicle.year,
                "status": vehicle.status,
                "mfg_year_month": vehicle.mfg_year_month,
                "date_of_registration": vehicle.date_of_registration,
                "vehicle_image": vehicle.vehicle_image.url if vehicle.vehicle_image else None,
            }
            for vehicle in page.object_list
        ]

        response = {
            "draw": draw,
            "recordsTotal": Vehicle.objects.count(),
            "recordsFiltered": vehicles.count(),
            "data": data
        }

        return JsonResponse(response, safe=False)

    except Exception as e:
        print("❌ API Error:", str(e))
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
    
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from .models import Vehicle, VehicleTypeDetail
import json

# Helper function for validation
def validate_vehicle_data(data):
    errors = {}
    license_plate_regex = r'^[A-Z]{2}-\d{3,4}-\d{2}$'
    
    # Validate license plate
    validator = RegexValidator(
        regex=license_plate_regex,
        message="License plate must be in the format 'GH-1234-21'.",
    )
    try:
        validator(data.get('license_plate', ''))
    except ValidationError as e:
        errors['license_plate'] = str(e.message)

    # Validate vehicle type
    if not data.get('vehicle_type_id') or not VehicleTypeDetail.objects.filter(id=data['vehicle_type_id']).exists():
        errors['vehicle_type'] = "Invalid or missing vehicle type."

    # Validate year
    if not isinstance(data.get('year'), int) or data['year'] < 1900:
        errors['year'] = "Invalid manufacturing year."
    
    # Validate status
    valid_statuses = ['available', 'maintenance', 'in_use']
    if data.get('status') not in valid_statuses:
        errors['status'] = "Invalid status value."
    
    return errors



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Vehicle

def get_vehicles(request, vehicle_id):
    """
    Retrieve details of a specific vehicle by ID.
    """
    try:
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        data = {
            "success": True,
            "license_plate": vehicle.license_plate,
            "vehicle_type": str(vehicle.vehicle_type) if vehicle.vehicle_type else None,  # ✅ Convert to string safely
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "mfg_year_month": str(vehicle.mfg_year_month) if vehicle.mfg_year_month else None,  # ✅ Convert to string
            "date_of_registration": vehicle.date_of_registration.strftime('%Y-%m-%d') if vehicle.date_of_registration else None,
            "vehicle_image": vehicle.vehicle_image.url if vehicle.vehicle_image else None,  # ✅ Prevent `.url` error
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)  # ✅ Handle errors safely



from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date
from .models import Vehicle, VehicleTypeDetail

@csrf_exempt
def add_vehicle(request):
    if request.method == 'POST':
        try:
            data = request.POST
            vehicle_image = request.FILES.get('vehicle_image')

            # Validate required fields
            required_fields = ['license_plate', 'vehicle_type', 'make', 'model', 'year', 'status']
            missing_fields = [field for field in required_fields if not data.get(field)]

            if missing_fields:
                return JsonResponse({"success": False, "error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

            # Save or retrieve VehicleTypeDetail
            vehicle_type, created = VehicleTypeDetail.objects.get_or_create(
                type=data['vehicle_type'], 
                make=data['make'], 
                model=data['model']
            )

            # Create the Vehicle instance
            vehicle = Vehicle.objects.create(
                license_plate=data['license_plate'],
                vehicle_type=vehicle_type,
                make=data['make'],  
                model=data['model'],
                year=int(data['year']),
                status=data['status'],
                mfg_year_month=parse_date(data.get('mfg_year_month')),  # Handle optional date
                date_of_registration=parse_date(data.get('date_of_registration')),
                vehicle_image=vehicle_image
            )

            return JsonResponse({
                "success": True,
                "message": "Vehicle added successfully",
                "vehicle_id": vehicle.id,
                "vehicle_type_id": vehicle_type.id
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Vehicle, VehicleTypeDetail

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Vehicle, VehicleTypeDetail

@csrf_exempt
def update_vehicle(request, vehicle_id):
    if request.method == "POST":  
        try:
            data = request.POST
            vehicle_image = request.FILES.get('vehicle_image')

            # Fetch the existing vehicle
            vehicle = get_object_or_404(Vehicle, id=vehicle_id)

            # Handle Vehicle Type
            vehicle_type, created = VehicleTypeDetail.objects.get_or_create(
                type=data.get('vehicle_type', vehicle.vehicle_type.type),
                make=data.get('make', vehicle.vehicle_type.make),
                model=data.get('model', vehicle.vehicle_type.model)
            )

            # Update fields (only update if a new value is provided)
            vehicle.license_plate = data.get('license_plate', vehicle.license_plate)
            vehicle.vehicle_type = vehicle_type
            vehicle.make = data.get('make', vehicle.make)
            vehicle.model = data.get('model', vehicle.model)
            vehicle.year = int(data.get('year', vehicle.year))
            vehicle.status = data.get('status', vehicle.status)

            # Handle optional date fields
            vehicle.mfg_year_month = parse_date(data.get('mfg_year_month', str(vehicle.mfg_year_month)))
            vehicle.date_of_registration = parse_date(data.get('date_of_registration', str(vehicle.date_of_registration)))

            # Update vehicle image if a new one is uploaded
            if vehicle_image:
                vehicle.vehicle_image = vehicle_image

            vehicle.save()  # Save the updates

            return JsonResponse({
                "success": True,
                "message": "Vehicle updated successfully",
                "vehicle_id": vehicle.id,
                "vehicle_type_id": vehicle.vehicle_type.id
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_vehicle(request, vehicle_id):
    if request.method == 'DELETE':
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        vehicle.delete()
        return JsonResponse({"success": True, "message": "Vehicle deleted successfully"})



################################################################################################################################


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
        "vehicles": vehicles,
        "drivers":drivers,
        "assistants":assistants
    }
    return render(request, "transport/delivery_schedule.html", context)


from django.shortcuts import render
from django.http import JsonResponse
from .models import DispatchRequest

def dispatch_list(request):
    dispatches = DispatchRequest.objects.select_related('vehicle', 'driver', 'assistant').all()

    data = []
    for dispatch in dispatches:
        data.append({
            "id": dispatch.id,
            "vehicle": dispatch.vehicle.make + " " + dispatch.vehicle.model,  # Adjust based on Vehicle model fields
            "license_plate": dispatch.vehicle.license_plate,
            "driver": dispatch.driver.name,  # Assuming the Driver model has a full_name field
            "assistant": dispatch.assistant.name if dispatch.assistant else "N/A",
            "destination": dispatch.destination,
            "status": dispatch.status.capitalize(),
            "schedule_date_time": dispatch.created_at.strftime("%Y-%m-%d %H:%M"),
        })

    return JsonResponse({"data": data})



def create_dispatch_request(request):
    """Handle creating a new dispatch request."""
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        driver_id = request.POST.get("driver")
        assistant_id = request.POST.get("assistant")
        destination = request.POST.get("destination")
        status = request.POST.get("status", "pending")
        trip_log = request.POST.get("trip_log", "")

        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        driver = get_object_or_404(Driver, id=driver_id)
        assistant = DriverAssistant.objects.filter(id=assistant_id).first() if assistant_id else None

        dispatch_request = DispatchRequest.objects.create(
            vehicle=vehicle,
            driver=driver,
            assistant=assistant,
            destination=destination,
            status=status,
            trip_log=trip_log
        )

        return redirect("dashboard_vehicles")  # Redirect to the dispatch request list page
    return JsonResponse({"error": "Invalid request method"}, status=400)



def get_dispatch(request, dispatch_id):
    dispatch = get_object_or_404(DispatchRequest, id=dispatch_id)
    data = {
        "vehicle": dispatch.vehicle.id,
        "driver": dispatch.driver.id,
        "assistant": dispatch.assistant.id if dispatch.assistant else "",
        "destination": dispatch.destination,
        "status": dispatch.status,
        "trip_log": dispatch.trip_log
    }
    return JsonResponse(data)



@csrf_exempt
def update_dispatch(request, dispatch_id):
    if request.method == "POST":
        try:
            data = request.POST

            # Get the dispatch request
            dispatch = get_object_or_404(DispatchRequest, id=dispatch_id)

            # Update fields only if new values are provided
            dispatch.vehicle = Vehicle.objects.get(id=data.get("vehicle", dispatch.vehicle.id))
            dispatch.driver = Driver.objects.get(id=data.get("driver", dispatch.driver.id))

            assistant_id = data.get("assistant")
            dispatch.assistant = DriverAssistant.objects.get(id=assistant_id) if assistant_id else None

            dispatch.destination = data.get("destination", dispatch.destination)
            dispatch.status = data.get("status", dispatch.status)
            dispatch.trip_log = data.get("trip_log", dispatch.trip_log)

            dispatch.save()

            return JsonResponse({"success": True, "message": "Dispatch updated successfully"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)



@csrf_exempt
def delete_dispatch(request, dispatch_id):
    if request.method == "POST":
        try:
            dispatch = get_object_or_404(DispatchRequest, id=dispatch_id)
            dispatch.delete()
            return JsonResponse({"success": True, "message": "Dispatch deleted successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)




def delete_dispatch_request(request, dispatch_id):
    """Handle deleting a dispatch request."""
    dispatch_request = get_object_or_404(DispatchRequest, id=dispatch_id)

    if request.method == "POST":
        dispatch_request.delete()
        return redirect("dashboard_vehicles")  # Redirect to the dispatch request list page

    return JsonResponse({"error": "Invalid request method"}, status=400)



####################################################################################################################################
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.core.serializers import serialize
import pandas as pd
from io import BytesIO
from .models import CurrentVehicleAssignment, Vehicle, Driver, DriverAssistant, ClientRequestInfo
import json

def driver_assistant_assignment_page(request):
    """
    View to render the assignments page.
    """
    assignments = CurrentVehicleAssignment.objects.all()
    vehicles = Vehicle.objects.all()
    drivers = Driver.objects.all()
    assistants = DriverAssistant.objects.all()
    client_requests = ClientRequestInfo.objects.all()

    # Extract choices from the model
    request_types = ClientRequestInfo.REQUEST_TYPES
    status_choices = ClientRequestInfo.status_choices

    context = {
        "path": request.path or "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "assignments": assignments,
        "vehicles": vehicles,
        "drivers": drivers,
        "assistants": assistants,
        "client_requests": client_requests,
        "request_types": request_types,  # Pass request type choices
        "status_choices": status_choices,  # Pass status choices
    }
    return render(request, "transport/driver_assistant_assignment.html", context)

def get_assignments(request):
    """
    API endpoint to fetch driver-vehicle assignments.
    """
    assignments = CurrentVehicleAssignment.objects.all().select_related("vehicle", "current_driver", "current_assistant", "vehicle__vehicle_type")
    
    data = []
    for assignment in assignments:
        data.append({
            "id": assignment.id,
            "current_driver": {"name": assignment.current_driver.name if assignment.current_driver else "N/A"},
            "current_assistant": {"name": assignment.current_assistant.name if assignment.current_assistant else "N/A"},
            "vehicle": {
                "license_plate": assignment.vehicle.license_plate if assignment.vehicle else "N/A",
                "vehicle_type": {
                    "type": assignment.vehicle.vehicle_type.type if assignment.vehicle and assignment.vehicle.vehicle_type else "N/A",
                    "make": assignment.vehicle.vehicle_type.make if assignment.vehicle and assignment.vehicle.vehicle_type else "N/A",
                    "model": assignment.vehicle.vehicle_type.model if assignment.vehicle and assignment.vehicle.vehicle_type else "N/A",
                }
            }
        })

        print(data)
    return JsonResponse({"data": data})


@csrf_exempt
def create_assignment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Check if the driver or assistant is already assigned
            if CurrentVehicleAssignment.objects.filter(current_driver_id=data["current_driver"]).exists():
                return JsonResponse({"error": "Driver is already assigned to another vehicle."}, status=400)
            
            if data.get("current_assistant") and CurrentVehicleAssignment.objects.filter(current_assistant_id=data["current_assistant"]).exists():
                return JsonResponse({"error": "Assistant is already assigned to another vehicle."}, status=400)
            
            assignment = CurrentVehicleAssignment.objects.create(
                current_driver_id=data["current_driver"],
                current_assistant_id=data.get("current_assistant"),  # Assistant might be optional
                vehicle_id=data["vehicle"]
            )
            return JsonResponse({"message": "Assignment created successfully", "id": assignment.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def update_assignment(request, assignment_id):
    if request.method == "PUT":
        try:
            assignment = CurrentVehicleAssignment.objects.get(id=assignment_id)
            data = json.loads(request.body)

            assignment.current_driver_id = data.get("current_driver", assignment.current_driver_id)
            assignment.current_assistant_id = data.get("current_assistant", assignment.current_assistant_id)
            assignment.vehicle_id = data.get("vehicle", assignment.vehicle_id)

            assignment.save()
            return JsonResponse({"message": "Assignment updated successfully"}, status=200)
        except CurrentVehicleAssignment.DoesNotExist:
            return JsonResponse({"error": "Assignment not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def delete_assignment(request, assignment_id):
    if request.method == "DELETE":
        try:
            assignment = CurrentVehicleAssignment.objects.get(id=assignment_id)
            assignment.delete()
            return JsonResponse({"message": "Assignment deleted"}, status=204)
        except CurrentVehicleAssignment.DoesNotExist:
            return JsonResponse({"error": "Assignment not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        


# vehicle Assignment

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DriverVehicleAssignment, Driver, DriverAssistant, Vehicle
from django.utils import timezone

def create_vehicle_assignment(request):
    if request.method == "POST":
        driver_id = request.POST.get("driver")
        assistant_id = request.POST.get("assistant")
        vehicle_id = request.POST.get("vehicle")

        # Validate the input
        if not driver_id or not vehicle_id:
            messages.error(request, "Driver and Vehicle are required!")
            return redirect("driver_assistant_assignment")

        try:
            driver = Driver.objects.get(id=driver_id)
            vehicle = Vehicle.objects.get(id=vehicle_id)
            assistant = DriverAssistant.objects.get(id=assistant_id) if assistant_id else None

            # Check if the vehicle is already assigned
            if DriverVehicleAssignment.objects.filter(assigned_vehicle=vehicle).exists():
                messages.error(request, "This vehicle is already assigned!")
                return redirect("driver_assistant_assignment_page")

            # Create the assignment
            assignment = CurrentVehicleAssignment.objects.create(
                current_driver=driver,
                vehicle=vehicle,
                current_assistant=assistant,
                updated_at=timezone.now()
            )

            messages.success(request, "Vehicle assigned successfully!")
            return redirect("driver_assistant_assignment_page")

        except (Driver.DoesNotExist, Vehicle.DoesNotExist, DriverAssistant.DoesNotExist):
            messages.error(request, "Invalid selection!")
            return redirect("add_assignment")

    return redirect("driver_assistant_assignment_page")


def update_vehicle_assignment(request, pk):
    assignment = get_object_or_404(DriverVehicleAssignment, pk=pk)

    if request.method == "POST":
        driver_id = request.POST.get("driver")
        assistant_id = request.POST.get("assistant")
        vehicle_id = request.POST.get("vehicle")

        if not driver_id or not vehicle_id:
            messages.error(request, "Driver and Vehicle are required!")
            return redirect("driver_assistant_assignment_page")

        try:
            driver = Driver.objects.get(id=driver_id)
            vehicle = Vehicle.objects.get(id=vehicle_id)
            assistant = DriverAssistant.objects.get(id=assistant_id) if assistant_id else None

            # Check if the vehicle is assigned to another driver
            if DriverVehicleAssignment.objects.filter(assigned_vehicle=vehicle).exclude(id=pk).exists():
                messages.error(request, "This vehicle is already assigned to another driver!")
                return redirect("driver_assistant_assignment_page")

            assignment.driver = driver
            assignment.assigned_vehicle = vehicle
            assignment.assigned_assistant = assistant
            assignment.assigned_date = timezone.now()
            assignment.save()

            messages.success(request, "Vehicle assignment updated successfully!")
            return redirect("driver_assistant_assignment_page")

        except (Driver.DoesNotExist, Vehicle.DoesNotExist, DriverAssistant.DoesNotExist):
            messages.error(request, "Invalid selection!")
            return redirect("driver_assistant_assignment_page")

    return render(request, "transport/edit_assignment.html", {"assignment": assignment})


def delete_vehicle_assignment(request, pk):
    assignment = get_object_or_404(DriverVehicleAssignment, pk=pk)

    if request.method == "POST":
        assignment.delete()
        messages.success(request, "Vehicle assignment deleted successfully!")
        return redirect("driver_assistant_assignment_page")

    return render(request, "transport/delete_assignment.html", {"assignment": assignment})



#####################################################################################################################################

from django.shortcuts import render, get_object_or_404
from .models import ClientRequestInfo

def client_requests_list(request):
    client_requests = ClientRequestInfo.objects.all().order_by('-created_at')  # Fetch all requests
    assignments = CurrentVehicleAssignment.objects.all()
    vehicles = Vehicle.objects.all()
    drivers = Driver.objects.all()
    assistants = DriverAssistant.objects.all()
    # client_requests = ClientRequestInfo.objects.all()

    # Extract choices from the model
    request_types = ClientRequestInfo.REQUEST_TYPES
    status_choices = ClientRequestInfo.status_choices

    context = {
        "path": request.path or "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        'client_requests': client_requests,
        "assignments": assignments,
        "vehicles": vehicles,
        "drivers": drivers,
        "assistants": assistants,
        # "client_requests": client_requests,
        "request_types": request_types,  # Pass request type choices
        "status_choices": status_choices,  # Pass status choices
    }

    return render(request, 'transport/client-requests.html', context)




@csrf_exempt
def create_client_request(request):
    if request.method == "POST":
        try:
            # Debugging: Print the request content type
            print("Content-Type:", request.content_type)

            if request.content_type == "application/json":
                data = json.loads(request.body)  # Parse JSON body
            else:
                data = request.POST  # Extract form data

            # Extract common data
            client_name = data.get("client_name")
            email = data.get("email")
            request_type = data.get("request_type")
            description = data.get("description")
            pickup_location = data.get("pickup_location", "")
            delivery_location = data.get("delivery_location", "")
            scheduled_date = parse_datetime(data.get("scheduled_date"))  
            vehicle_id = data.get("vehicle_id")
            driver_id = data.get("driver_id")
            assistant_id = data.get("assistant_id")
            trip_log = data.get("trip_log", "")

            if isinstance(scheduled_date, str):
                scheduled_date = datetime.strptime(scheduled_date, "%Y-%m-%dT%H:%M")

            scheduled_date = timezone.make_aware(scheduled_date)  # This handles both cases


            # Get vehicle instance
            vehicle = Vehicle.objects.get(id=vehicle_id)

            # Save in ClientRequestDetail
            client_request = ClientRequestDetail.objects.create(
                client_name=client_name,
                email=email,
                request_type=request_type,
                vehicle=vehicle,
                description=description,
                pickup_location=pickup_location,
                delivery_location=delivery_location,
                scheduled_date=scheduled_date
            )

            # Save in DispatchRequest
            driver = Driver.objects.get(id=driver_id)
            assistant = DriverAssistant.objects.get(id=assistant_id) if assistant_id else None
            dispatch_request = DispatchRequest.objects.create(
                vehicle=vehicle,
                driver=driver,
                assistant=assistant,
                destination=delivery_location
            )

            # Save in ClientRequestInfo
            client_request_info = ClientRequestInfo.objects.create(
                client_name=client_name,
                email=email,
                request_type=request_type,
                scheduled_date=scheduled_date,
                description=description,
                vehicle_license_plate=vehicle.license_plate,
                vehicle_type=vehicle.vehicle_type,
                vehicle_make=vehicle.make,
                vehicle_model=vehicle.model,
                driver=driver,
                assistant=assistant,
                pickup_location=pickup_location,
                delivery_location=delivery_location

            )

            return JsonResponse({"message": "Request saved successfully", "request_id": client_request_info.id}, status=201)

        except Vehicle.DoesNotExist:
            return JsonResponse({"error": "Invalid vehicle ID"}, status=400)
        except Driver.DoesNotExist:
            return JsonResponse({"error": "Invalid driver ID"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



from django.http import JsonResponse
# from .models import ClientRequest

def get_client_request_details(request, request_id):
    client_request = ClientRequestDetail.objects.get(id=request_id)
    data = {
        "client_name": client_request.client_name,
        "email": client_request.email,
        "request_type": client_request.request_type,
        "scheduled_date": client_request.scheduled_date.strftime("%Y-%m-%dT%H:%M"),
        "description": client_request.description,
        "vehicle_license_plate": client_request.vehicle_license_plate,
        "vehicle_type": client_request.vehicle_type,
        "vehicle_make": client_request.vehicle_make,
        "vehicle_model": client_request.vehicle_model,
        "vehicle_id": client_request.vehicle.id if client_request.vehicle else "",
        "driver_id": client_request.driver.id if client_request.driver else "",
        "assistant_id": client_request.assistant.id if client_request.assistant else "",
        "pickup_location": client_request.pickup_location,
        "delivery_location": client_request.delivery_location,
        "status": client_request.status,
        "trip_log": client_request.trip_log,
    }
    return JsonResponse(data)

def fetch_client_requests(request):
    client_requests = list(ClientRequestInfo.objects.values())
    return JsonResponse(client_requests, safe=False)

@csrf_exempt
def update_client_request(request, request_id):
    """ Update a client request and convert inputs to uppercase """
    if request.method == "PUT":
        try:
            client_request = get_object_or_404(ClientRequestInfo, id=request_id)
            data = json.loads(request.body)

            client_request.status = data.get("status", client_request.status).upper()
            client_request.scheduled_date = parse_datetime(data.get("scheduled_date", str(client_request.scheduled_date)))
            client_request.description = data.get("description", client_request.description).upper()
            client_request.pickup_location = data.get("pickup_location", client_request.pickup_location).upper()
            client_request.delivery_location = data.get("delivery_location", client_request.delivery_location).upper()
            client_request.trip_log = data.get("trip_log", client_request.trip_log).upper()

            client_request.save()
            return JsonResponse({"message": "REQUEST UPDATED SUCCESSFULLY"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e).upper()}, status=500)

    return JsonResponse({"error": "INVALID REQUEST METHOD"}, status=405)


@csrf_exempt
def delete_client_request(request, request_id):
    """ Delete a client request """
    if request.method == "DELETE":
        try:
            client_request = get_object_or_404(ClientRequestInfo, id=request_id)
            client_request.delete()
            return JsonResponse({"message": "Request deleted successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)





###################################################################################################################################



def inventory_view(request):
    inventories = InventoryItem.objects.all()  # Fetch all inventory items
    categories = ItemCategory.choices
    departments = Department.objects.all()

    context = {
        "path": request.path if request.path else "",
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "inventories": inventories, 
        "categories": categories  ,# Pass inventories to the template
        "TransactionType": TransactionType.choices,
        "departments": departments

        
    }
    return render(request, "transport/requested-inventories.html", context)

# def requested_inventory(request):
#     inventories = InventoryItem.objects.all()  # Fetch all inventory items
#     employees = Employee.objects.all()
#     departments = Department.objects.all()
#     inventory_request = InventoryRequest.objects.all()

#     context = {
#         "path": request.path if request.path else "",
#         "sidebar_items": sidebar.Sidebar.sidebar_items,
#         "inventories": inventories,  # Pass inventories to the template
#         "employees": employees,
#         "departments": departments,
#         "inventory_request": inventory_request,
#         "TransactionType": TransactionType
#     }
#     return render(request, "inventory/requested-inventories.html", context)



def get_inventory_requests(request):
    """Retrieve all inventory requests where to_department is Transport"""
    inventory_requests = InventoryRequest.objects.filter(to_department__name="Transport").select_related(
        'item', 'from_department', 'to_department', 'employee'
    )

    data = [
        {
            "id": inv.id,
            "item": inv.item.name,
            "category": inv.category,
            "description": inv.description,
            "quantity": inv.quantity,
            "transaction_type": inv.transaction_type,
            "from_department": inv.from_department.name if inv.from_department else None,
            "to_department": inv.to_department.name if inv.to_department else None,
            "employee_name": inv.employee_name,
            "employee_phone": inv.employee_phone,
            "employee_ghana_card_number": inv.employee_ghana_card_number,
            "employee_position": inv.employee_position,
            "created_at": inv.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": inv.remarks,
        }
        for inv in inventory_requests
    ]

    print(data)  
    return JsonResponse({'data': data})


    print(data) 
    return JsonResponse({'data': data})
def get_inventory_request_detail(request, id):
    """Retrieve a specific inventory request by ID"""
    inventory_request = get_object_or_404(InventoryRequest, id=id)
    
    data = {
        "id": inventory_request.id,
        "item": inventory_request.item.name,
        "category": inventory_request.category,
        "description": inventory_request.description,
        "quantity": inventory_request.quantity,
        "transaction_type": inventory_request.transaction_type,
        "from_department": inventory_request.from_department.name if inventory_request.from_department else None,
        "to_department": inventory_request.to_department.name if inventory_request.to_department else None,
        "employee_name": inventory_request.employee_name,
        "employee_phone": inventory_request.employee_phone,
        "employee_ghana_card_number": inventory_request.employee_ghana_card_number,
        "employee_position": inventory_request.employee_position,
        "created_at": inventory_request.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "remarks": inventory_request.remarks,
    }

    return JsonResponse(data)



@csrf_exempt
def add_inventory_request(request):
    """Handle add request for inventory"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Access data using updated keys
            item = InventoryItem.objects.get(id=data['item'])  # 'item' instead of 'inventory_item'
            from_department = Department.objects.get(id=data['from_department']) if data['from_department'] else None
            to_department = Department.objects.get(id=data['to_department']) if data['to_department'] else None
            employee = Employee.objects.get(id=data['employee']) if data['employee'] else None
            
            # Create the InventoryRequest object
            inventory_request = InventoryRequest(
                item=item,
                category=data['category'],
                description=data.get('description', ''),
                quantity=data['requested_quantity'],  # Using 'requested_quantity' instead of 'quantity'
                transaction_type=data['transaction_type'],
                from_department=from_department,
                to_department=to_department,
                employee=employee,
                employee_name=data.get('employee_name', ''),
                employee_phone=data.get('employee_phone', ''),
                employee_ghana_card_number=data.get('employee_ghana_card_number', ''),
                employee_position=data.get('employee_position', ''),
                remarks=data.get('remarks', '')
            )
            inventory_request.save()

            return JsonResponse({'status': 'success', 'message': 'Inventory request added successfully'})

        except InventoryItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item does not exist'})
        except Department.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Department does not exist'})
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})


# @csrf_exempt
# def update_inventory_request(request):
#     """Handle update request for inventory"""
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             inventory_request = InventoryRequest.objects.get(id=data['id'])
            
#             inventory_request.item = InventoryItem.objects.get(id=data['item'])
#             inventory_request.category = data['category']
#             inventory_request.description = data.get('description', '')
#             inventory_request.quantity = data['quantity']
#             inventory_request.transaction_type = data['transaction_type']
#             inventory_request.from_department = Department.objects.get(id=data['from_department']) if data['from_department'] else None
#             inventory_request.to_department = Department.objects.get(id=data['to_department']) if data['to_department'] else None
#             inventory_request.employee = Employee.objects.get(id=data['employee']) if data['employee'] else None
#             inventory_request.employee_name = data.get('employee_name', '')
#             inventory_request.employee_phone = data.get('employee_phone', '')
#             inventory_request.employee_ghana_card_number = data.get('employee_ghana_card_number', '')
#             inventory_request.employee_position = data.get('employee_position', '')
#             inventory_request.remarks = data.get('remarks', '')

#             inventory_request.save()

#             return JsonResponse({'status': 'success', 'message': 'Inventory request updated successfully'})

#         except InventoryRequest.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Inventory request not found'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})


@csrf_exempt
def update_inventory_request(request):
    """Handle the update of an inventory request"""
    if request.method == 'POST':
        try:
            # Get the data sent from the frontend
            data = json.loads(request.body)
            inventory_id = data.get('id')  # Get the ID from the request body

            # Fetch the inventory request by ID
            inventory_request = InventoryRequest.objects.get(id=inventory_id)

            # Update the fields
            inventory_request.item = data.get('item')
            inventory_request.category = data.get('category')
            inventory_request.description = data.get('description')
            inventory_request.quantity = data.get('quantity')
            inventory_request.transaction_type = data.get('transaction_type')
            inventory_request.from_department = data.get('from_department')
            inventory_request.to_department = data.get('to_department')
            inventory_request.employee_name = data.get('employee_name')
            inventory_request.employee_phone = data.get('employee_phone')
            inventory_request.employee_ghana_card_number = data.get('employee_ghana_card_number')
            inventory_request.employee_position = data.get('employee_position')
            inventory_request.remarks = data.get('remarks')

            # Save the updated inventory request
            inventory_request.save()

            return JsonResponse({'status': 'success', 'message': 'Inventory request updated successfully'})

        except InventoryRequest.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Inventory request not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})
        

@csrf_exempt
def delete_inventory_request(request):
    """Handle delete request for inventory"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inventory_request = InventoryRequest.objects.get(id=data['id'])
            inventory_request.delete()

            return JsonResponse({'status': 'success', 'message': 'Inventory request deleted successfully'})

        except InventoryRequest.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Inventory request not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})




####################################################################################################################################




































# 🚘 Vehicle Management View
# def vehicle_view(request):
#     vehicles = Vehicle.objects.all()  
#     drivers = Driver.objects.all()
#     assistant = DriverAssistant.objects.all()
#     maintenance_requests = MaintenanceRequest.objects.all()

#     for driver in drivers:
#         print(driver.name)

#     context = {
#         "path": request.path or "",
#         "sidebar_items": sidebar.Sidebar.sidebar_items,
#         "vehicles": vehicles,
#         # "assignment": MaintenanceRequest,
#         "drivers": drivers,
#         "assistants": assistant,
#         # "maintenance_requests": maintenance_requests
        
#     }
#     return render(request, "transport/vehicles.html", context)


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

###############################################################################################################################

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

########################################################################################################################################

def maintenance_request(request):
    """
    View to handle maintenance requests and update vehicle status automatically.
    """
    maintenance_requests = MaintenanceRequest.objects.all()
    vehicles = Vehicle.objects.all()
    inventories = InventoryItem.objects.all()  # Fetch all inventory items
    employees = Employee.objects.all()
    departments = Department.objects.all()
    inventory_request = InventoryRequest.objects.all()

    context = {
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "maintenance_requests": maintenance_requests,
        "vehicles": vehicles,
        "inventories": inventories,  # Pass inventories to the template
        "employees": employees,
        "departments": departments,
        "inventory_request": inventory_request,
        "TransactionType": TransactionType
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
    elif instance.status == "pending":
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



###########################################################################################################


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import MaintenanceRequest, Vehicle
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import MaintenanceRequest, Vehicle

# Create a new maintenance request
def create_maintenance_request(request):
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        requested_by = request.POST.get("requested_by")
        category = request.POST.get("category")
        description = request.POST.get("description")
        status = request.POST.get("status", "pending")

        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        maintenance_request = MaintenanceRequest.objects.create(
            vehicle=vehicle,
            requested_by=requested_by,
            category=category,
            description=description,
            status=status,
        )
        return redirect("create_maintenance_request")  # Redirect to maintenance list view

    vehicles = Vehicle.objects.all()
    return render(request, "transport/maintenance-request.html", {"vehicles": vehicles})







# Fetch all maintenance requests (for DataTable)
def get_maintenance_requests(request):
    maintenance_requests = MaintenanceRequest.objects.all().values(
        "id", "vehicle__license_plate", "requested_by", "category", "description", "status", "created_at", "updated_at"
    )
    return JsonResponse({"data": list(maintenance_requests)}, safe=False)


# Create a new maintenance request (via AJAX)
@csrf_exempt  # Remove this if CSRF protection is needed
def create_new_maintenance_request(request):
    if request.method == "POST":
        try:
            print("Received POST request for maintenance request creation ✅")

            # Parse POST data
            vehicle_id = request.POST.get("vehicle")
            requested_by = request.POST.get("requested_by")
            category = request.POST.get("category")
            description = request.POST.get("description")
            status = request.POST.get("status", "pending")

            print(f"Received data - Vehicle ID: {vehicle_id}, Requested By: {requested_by}, Category: {category}, Description: {description}, Status: {status}")

            # Ensure vehicle exists
            vehicle = get_object_or_404(Vehicle, id=vehicle_id)
            print(f"Vehicle found ✅: {vehicle}")

            # Create Maintenance Request
            maintenance_request = MaintenanceRequest.objects.create(
                vehicle=vehicle,
                requested_by=requested_by,
                category=category,
                description=description,
                status=status,
            )

            print(f"Maintenance Request Created Successfully ✅ - ID: {maintenance_request.id}")

            return JsonResponse({"message": "Maintenance request created successfully", "id": maintenance_request.id}, status=201)

        except Exception as e:
            print(f"Error while creating maintenance request ❌: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)

    print("Invalid request method ❌ - Only POST is allowed")
    return HttpResponseNotAllowed(["POST"])




# Update a maintenance request
@csrf_exempt
def update_maintenance_request(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, id=request_id)

    if request.method == "POST":
        maintenance_request.vehicle_id = request.POST.get("vehicle")
        maintenance_request.requested_by = request.POST.get("requested_by")
        maintenance_request.category = request.POST.get("category")
        maintenance_request.description = request.POST.get("description")
        maintenance_request.status = request.POST.get("status")
        maintenance_request.save()

        return JsonResponse({"message": "Maintenance request updated successfully"})

    return HttpResponseNotAllowed(["POST"])


# Delete a maintenance request
@csrf_exempt
def delete_maintenance_request(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, id=request_id)

    if request.method == "POST":
        maintenance_request.delete()
        return JsonResponse({"message": "Maintenance request deleted successfully"})

    return HttpResponseNotAllowed(["POST"])

#############################################################################################################























# # from django.shortcuts import render
# # from .models import CurrentVehicleAssignment, Vehicle, Driver, DriverAssistant
# def driver_assistant_assignment(request):
#     """
#     View to handle driver-vehicle assignments, ensuring maintenance vehicles are not assigned.
#     """
#     assignments = CurrentVehicleAssignment.objects.all()
#     vehicles = Vehicle.objects.all()
#     drivers = Driver.objects.all()
#     assistants = DriverAssistant.objects.all()
#     client_requests = ClientRequestInfo.objects.all()

#     # Extract choices from the model
#     request_types = ClientRequestInfo.REQUEST_TYPES
#     status_choices = ClientRequestInfo.status_choices

#     context = {
#         "path": request.path or "",
#         "sidebar_items": sidebar.Sidebar.sidebar_items,
#         "assignments": assignments,
#         "vehicles": vehicles,
#         "drivers": drivers,
#         "assistants": assistants,
#         "client_requests": client_requests,
#         "request_types": request_types,  # Pass request type choices
#         "status_choices": status_choices,  # Pass status choices
#     }

#     return render(request, "transport/driver_assistant_assignment.html", context)



# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404, render
# from .models import CurrentVehicleAssignment, Vehicle, Driver, DriverAssistant

# def get_vehicle_assignment(request, vehicle_id):
#     """Fetch assigned driver and assistant based on selected vehicle"""
#     assignment = get_object_or_404(CurrentVehicleAssignment, vehicle_id=vehicle_id)

#     data = {
#         "vehicle_type": assignment.vehicle.vehicle_type,
#         "make": assignment.vehicle.make,
#         "model": assignment.vehicle.model,
#         "license_plate": assignment.vehicle.license_plate,
#         "driver_id": assignment.current_driver.id if assignment.current_driver else None,
#         "driver_name": assignment.current_driver.name if assignment.current_driver else "",
#         "assistant_id": assignment.current_assistant.id if assignment.current_assistant else None,
#         "assistant_name": assignment.current_assistant.name if assignment.current_assistant else "",
#     }

#     return JsonResponse(data)









# ######################################################################################################


# ############################################################################
#maintenance_request

#########################################################################################

#######################################################################################################
#Dispatch Request

def create_dispatch_request(request):
    """Handle creating a new dispatch request."""
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        driver_id = request.POST.get("driver")
        assistant_id = request.POST.get("assistant")
        destination = request.POST.get("destination")
        status = request.POST.get("status", "pending")
        trip_log = request.POST.get("trip_log", "")

        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        driver = get_object_or_404(Driver, id=driver_id)
        assistant = DriverAssistant.objects.filter(id=assistant_id).first() if assistant_id else None

        dispatch_request = DispatchRequest.objects.create(
            vehicle=vehicle,
            driver=driver,
            assistant=assistant,
            destination=destination,
            status=status,
            trip_log=trip_log
        )

        return redirect("dashboard_vehicles")  # Redirect to the dispatch request list page
    return JsonResponse({"error": "Invalid request method"}, status=400)

def update_dispatch_request(request):
    """Handle updating an existing dispatch request."""
    if request.method == "POST":
        dispatch_id = request.POST.get("dispatch_id")
        dispatch_request = get_object_or_404(DispatchRequest, id=dispatch_id)

        dispatch_request.vehicle = get_object_or_404(Vehicle, id=request.POST.get("vehicle"))
        dispatch_request.driver = get_object_or_404(Driver, id=request.POST.get("driver"))
        assistant_id = request.POST.get("assistant")
        dispatch_request.assistant = get_object_or_404(DriverAssistant, id=assistant_id) if assistant_id else None
        dispatch_request.destination = request.POST.get("destination")
        dispatch_request.status = request.POST.get("status")
        dispatch_request.trip_log = request.POST.get("trip_log", "")

        dispatch_request.save()
        return redirect("dashboard_vehicles")  # Redirect to the appropriate page

    return JsonResponse({"error": "Invalid request method"}, status=405)


def delete_dispatch_request(request, dispatch_id):
    """Handle deleting a dispatch request."""
    dispatch_request = get_object_or_404(DispatchRequest, id=dispatch_id)

    if request.method == "POST":
        dispatch_request.delete()
        return redirect("dashboard_vehicles")  # Redirect to the dispatch request list page

    return JsonResponse({"error": "Invalid request method"}, status=400)


def transport_data(request):
    total_vehicles = Vehicle.objects.count()
    total_drivers = Driver.objects.count()
    total_assignments = DriverVehicleAssignment.objects.count()

    vehicle_status = Vehicle.objects.values('status').annotate(count=models.Count('status'))
    maintenance_requests = MaintenanceRequest.objects.values('status').annotate(count=models.Count('status'))
    dispatch_requests = DispatchRequest.objects.values('status').annotate(count=models.Count('status'))
    
    top_vehicles = DriverVehicleAssignment.objects.values('assigned_vehicle__license_plate').annotate(
        count=models.Count('assigned_vehicle')
    ).order_by('-count')[:5]

    response_data = {
        "total_vehicles": total_vehicles,
        "total_drivers": total_drivers,
        "total_assignments": total_assignments,
        "vehicle_status": list(vehicle_status),
        "maintenance_requests": list(maintenance_requests),
        "dispatch_requests": list(dispatch_requests),
        "top_vehicles": list(top_vehicles),
    }
    return JsonResponse(response_data)
