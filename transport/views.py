
from django.shortcuts import render
from utils import  sidebar
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vehicle
from .serializers import VehicleSerializer

def transport_view(request):
    # print(sidebar.Sidebar.sidebar_items)
    context = {
        "path": request.path if request.path else "",  # Ensure path is always a string
        "sidebar_items": sidebar.Sidebar.sidebar_items
    }
    return render(request, "transport/dashboard.html",context)

def vehicle_view(request):
    vehicles = Vehicle.objects.all()  # Fetch all vehicles from the database
    
    context = {
        "path": request.path if request.path else "",  # Ensure path is always a string
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "vehicles": vehicles,  # Pass vehicle data to template
    }
    return render(request, "transport/vehicles.html", context)




def vehicle_view(request):
    vehicles = Vehicle.objects.all()  # Fetch all vehicles from the database
    
    context = {
        "path": request.path if request.path else "",  # Ensure path is always a string
        "sidebar_items": sidebar.Sidebar.sidebar_items,
        "vehicles": vehicles,  # Pass vehicle data to template
    }
    return render(request, "transport/vehicles.html", context)


# 🚀 API Endpoints for CRUD Operations 🚀 #

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
def vehicle_detail(request, vehicle_id):
    """Retrieve a specific vehicle"""
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    serializer = VehicleSerializer(vehicle)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def vehicle_update(request, vehicle_id):
    """Update vehicle details"""
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    serializer = VehicleSerializer(vehicle, data=request.data, partial=True)  # Allow partial update
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def vehicle_delete(request, vehicle_id):
    """Delete a vehicle"""
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    vehicle.delete()
    return Response({"message": "Vehicle deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
